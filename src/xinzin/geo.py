import json
import os
import subprocess
import tempfile
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from check_url import BASE_PORT, build_run_config, wait_for_ports

AGREE = 2


def parse_trace(text):
    for line in text.splitlines():
        if line.startswith("loc="):
            return line[4:].strip()
    return None


def parse_json(key):
    return lambda text: json.loads(text).get(key)


SERVICES = [
    ("cloudflare", "https://www.cloudflare.com/cdn-cgi/trace", parse_trace),
    ("ip-api.com", "http://ip-api.com/json/?fields=status,countryCode", parse_json("countryCode")),
    ("ipwho.is", "https://ipwho.is/", parse_json("country_code")),
    ("ipinfo.io", "https://ipinfo.io/json", parse_json("country")),
    ("ipapi.co", "https://ipapi.co/json/", parse_json("country_code")),
]


def flag(code):
    if not code or len(code) != 2 or not code.isalpha():
        return "🇽🇽"
    return "".join(chr(0x1F1E6 + ord(letter) - 65) for letter in code.upper())


def fetch_text(opener, url, timeout):
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with opener.open(request, timeout=timeout) as response:
        return response.read(20000).decode("utf-8", errors="replace")


def lookup_country(port, timeout):
    proxy = "http://127.0.0.1:" + str(port)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    answers = {}
    for name, url, extract in SERVICES:
        try:
            code = extract(fetch_text(opener, url, timeout))
        except Exception:
            continue
        if isinstance(code, str) and len(code) == 2 and code.isalpha():
            answers[name] = code.upper()
        if answers and Counter(answers.values()).most_common(1)[0][1] >= AGREE:
            break
    return answers


def decide(answers):
    if not answers:
        return ""
    code, count = Counter(answers.values()).most_common(1)[0]
    if code == "RU" and count < AGREE:
        return ""
    return code


def run_batch(batch, timeout):
    outbounds = [outbound for _, outbound in batch]
    config = build_run_config(outbounds)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(config, handle)
        path = handle.name
    process = subprocess.Popen(["sing-box", "run", "-c", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    results = [{} for _ in batch]
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


def classify(answers):
    if not answers:
        return "no answers"
    if len(set(answers.values())) > 1:
        return "sources disagree"
    if len(answers) == 1:
        return "one source only"
    return "sources agree"


def detect_countries(pairs, batch_size, timeout):
    stats = Counter()
    examples = []
    for start in range(0, len(pairs), batch_size):
        batch = pairs[start:start + batch_size]
        for (node, _), answers in zip(batch, run_batch(batch, timeout)):
            node["country"] = decide(answers)
            kind = classify(answers)
            stats[kind] += 1
            if kind == "sources disagree" and len(examples) < 15:
                examples.append(node["address"] + " -> " + str(answers) + " => " + (node["country"] or "unknown"))
        print("  batch " + str(start // batch_size + 1) + " done", flush=True)
    for example in examples:
        print("  split: " + example)
    return stats
