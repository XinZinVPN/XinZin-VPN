import json
import os
import random
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from singbox import base_config

BASE_PORT = 20000
TEST_URL = "https://www.wikipedia.org/"
MIN_BYTES = 10000


def build_run_config(outbounds):
    config = base_config(outbounds)
    for index, outbound in enumerate(outbounds):
        inbound_tag = "in-" + str(index)
        config["inbounds"].append({"type": "mixed", "tag": inbound_tag, "listen": "127.0.0.1", "listen_port": BASE_PORT + index})
        config["route"]["rules"].append({"inbound": [inbound_tag], "action": "route", "outbound": outbound["tag"]})
    return config


def wait_for_ports(process, last_port, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if process.poll() is not None:
            return False
        try:
            with socket.create_connection(("127.0.0.1", last_port), timeout=1):
                return True
        except OSError:
            time.sleep(0.3)
    return False


def fetch_once(port, timeout):
    proxy = "http://127.0.0.1:" + str(port)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    url = TEST_URL + "?xz=" + str(random.randint(1, 10**9))
    headers = {"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache", "Accept-Encoding": "identity"}
    request = urllib.request.Request(url, headers=headers)
    limit = time.time() + timeout
    body = b""
    with opener.open(request, timeout=timeout) as response:
        status = response.status
        while True:
            chunk = response.read(16384)
            if not chunk:
                break
            body += chunk
            if time.time() > limit:
                return "slow"
    if status != 200:
        return "http " + str(status)
    if len(body) < MIN_BYTES or b"Wikipedia" not in body:
        return "bad content"
    return ""


def test_node(port, timeout, retries):
    reason = ""
    for _ in range(retries + 1):
        started = time.time()
        try:
            reason = fetch_once(port, timeout)
        except urllib.error.HTTPError as error:
            reason = "http " + str(error.code)
        except Exception as error:
            reason = type(error).__name__
        if not reason:
            return True, "", round(time.time() - started, 2)
    return False, reason, 0


def run_batch(batch, timeout, retries):
    outbounds = [outbound for _, outbound in batch]
    config = build_run_config(outbounds)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(config, handle)
        path = handle.name
    process = subprocess.Popen(["sing-box", "run", "-c", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    results = []
    try:
        if not wait_for_ports(process, BASE_PORT + len(batch) - 1):
            return [(node, False, "sing-box did not start", 0) for node, _ in batch]
        with ThreadPoolExecutor(max_workers=len(batch)) as pool:
            futures = [pool.submit(test_node, BASE_PORT + index, timeout, retries) for index in range(len(batch))]
            for (node, _), future in zip(batch, futures):
                ok, reason, latency = future.result()
                results.append((node, ok, reason, latency))
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        os.remove(path)
    return results


def check_url(pairs, batch_size, timeout, retries):
    passed = []
    reasons = Counter()
    for start in range(0, len(pairs), batch_size):
        batch = pairs[start:start + batch_size]
        for node, ok, reason, latency in run_batch(batch, timeout, retries):
            if ok:
                node["latency"] = latency
                passed.append(node)
            else:
                reasons[reason] += 1
        print("  batch " + str(start // batch_size + 1) + ": passed so far " + str(len(passed)), flush=True)
    return passed, reasons
