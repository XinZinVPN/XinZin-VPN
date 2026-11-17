import json
import os
import subprocess
import tempfile
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from check_url import BASE_PORT, build_run_config, wait_for_ports

SERVICES = [
    ("https://ipwho.is/", lambda data: data.get("country_code") if data.get("success", True) else None),
    ("https://ipapi.co/json/", lambda data: data.get("country_code")),
    ("http://ip-api.com/json/?fields=status,countryCode", lambda data: data.get("countryCode") if data.get("status") == "success" else None),
]


def flag(code):
    if not code or len(code) != 2 or not code.isalpha():
        return "🇽🇽"
    return "".join(chr(0x1F1E6 + ord(letter) - 65) for letter in code.upper())


def lookup_country(port, timeout):
    proxy = "http://127.0.0.1:" + str(port)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    for url, extract in SERVICES:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with opener.open(request, timeout=timeout) as response:
                data = json.loads(response.read(20000).decode("utf-8", errors="replace"))
            code = extract(data)
            if isinstance(code, str) and len(code) == 2 and code.isalpha():
                return code.upper(), url
        except Exception:
            continue
    return "", ""


def run_batch(batch, timeout):
    outbounds = [outbound for _, outbound in batch]
    config = build_run_config(outbounds)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(config, handle)
        path = handle.name
    process = subprocess.Popen(["sing-box", "run", "-c", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    results = [("", "")] * len(batch)
    try:
        if wait_for_ports(process, BASE_PORT + len(batch) - 1):
            with ThreadPoolExecutor(max_workers=len(batch)) as pool:
                futures = [pool.submit(lookup_country, BASE_PORT + index, timeout) for index in range(len(batch))]
                results = [future.result() for future in futures]
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        os.remove(path)
    return results


def detect_countries(pairs, batch_size, timeout):
    services_used = Counter()
    for start in range(0, len(pairs), batch_size):
        batch = pairs[start:start + batch_size]
        for (node, _), (code, service) in zip(batch, run_batch(batch, timeout)):
            node["country"] = code
            services_used[service or "none"] += 1
        print("  batch " + str(start // batch_size + 1) + " done", flush=True)
    return services_used
