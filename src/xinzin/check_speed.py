import json
import os
import subprocess
import tempfile
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from check_url import BASE_PORT, build_run_config, wait_for_ports

SPEED_URL = "https://speed.cloudflare.com/__down?bytes="


def measure_download(port, size, timeout):
    proxy = "http://127.0.0.1:" + str(port)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    headers = {"User-Agent": "Mozilla/5.0", "Accept-Encoding": "identity"}
    request = urllib.request.Request(SPEED_URL + str(size), headers=headers)
    started = time.time()
    received = 0
    try:
        with opener.open(request, timeout=timeout) as response:
            while True:
                chunk = response.read(65536)
                if not chunk:
                    break
                received += len(chunk)
                if time.time() - started > timeout:
                    return 0.0, "slow"
    except Exception as error:
        return 0.0, type(error).__name__
    elapsed = max(time.time() - started, 0.001)
    if received < size:
        return 0.0, "short"
    return round(size * 8 / 1000000 / elapsed, 2), ""


def run_batch(batch, size, timeout, parallel):
    outbounds = [outbound for _, outbound in batch]
    config = build_run_config(outbounds)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(config, handle)
        path = handle.name
    process = subprocess.Popen(["sing-box", "run", "-c", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    results = [(0.0, "sing-box did not start")] * len(batch)
    try:
        if wait_for_ports(process, BASE_PORT + len(batch) - 1):
            with ThreadPoolExecutor(max_workers=parallel) as pool:
                futures = [pool.submit(measure_download, BASE_PORT + index, size, timeout) for index in range(len(batch))]
                results = [future.result() for future in futures]
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        os.remove(path)
    return results


def check_speed(pairs, batch_size, size, timeout, parallel, min_mbps):
    passed = []
    reasons = Counter()
    speeds = []
    for start in range(0, len(pairs), batch_size):
        batch = pairs[start:start + batch_size]
        for (node, outbound), (mbps, reason) in zip(batch, run_batch(batch, size, timeout, parallel)):
            node["speed"] = mbps
            if reason:
                reasons[reason] += 1
                continue
            speeds.append(mbps)
            if mbps < min_mbps:
                reasons["below minimum"] += 1
                continue
            passed.append((node, outbound))
        print("  batch " + str(start // batch_size + 1) + ": passed so far " + str(len(passed)), flush=True)
    return passed, reasons, speeds
