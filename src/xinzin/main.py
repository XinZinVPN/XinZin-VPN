import base64
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

from parsers import parse_link

import time

from check_tcp import check_tcp
from outbounds import build_outbound
from singbox import filter_valid
from check_url import check_url
from geo import detect_countries
from check_speed import check_speed

import sys

from render import render
from publish import count_published, validate, write_output

ROOT = Path(__file__).resolve().parents[2]


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": "XinZinVPN"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def decode_if_base64(text):
    if "://" in text:
        return text
    try:
        compact = "".join(text.split())
        compact += "=" * (-len(compact) % 4)
        return base64.b64decode(compact).decode("utf-8", errors="replace")
    except Exception:
        return text


def get_lines(text):
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            lines.append(line)
    return lines


def main():
    config = yaml.safe_load((ROOT / "config" / "sources.yaml").read_text(encoding="utf-8"))
    sources = sorted(config["sources"], key=lambda source: source["priority"])
    unique = {}
    broken_samples = []
    print("=== XinZinVPN: parse and dedupe report ===")
    for source in sources:
        name = source["name"]
        try:
            text = decode_if_base64(download(source["url"]))
        except Exception as error:
            print(f"[FAIL] {name}: {error}")
            continue
        lines = get_lines(text)
        added = 0
        duplicates = 0
        broken = 0
        for line in lines:
            node = parse_link(line)
            if node is None:
                broken += 1
                if len(broken_samples) < 5:
                    broken_samples.append(line[:80])
                continue
            key = (node["address"], node["port"])
            if key in unique:
                duplicates += 1
                continue
            unique[key] = node
            added += 1
        print(f"[OK] {name} (priority {source['priority']}): {len(lines)} lines, new {added}, duplicates {duplicates}, unparsed {broken}")
    protocols = Counter(node["protocol"] for node in unique.values())
    print(f"=== unique servers: {len(unique)} ===")
    print(f"=== by protocol: {dict(protocols)} ===")
    if broken_samples:
        print("=== examples of unparsed lines ===")
        for sample in broken_samples:
            print(sample)
    settings = yaml.safe_load((ROOT / "config" / "settings.yaml").read_text(encoding="utf-8"))
    started = time.time()
    alive, skipped = check_tcp(list(unique.values()), settings["tcp_timeout_seconds"], settings["tcp_parallel"])
    duration = round(time.time() - started)
    print("=== TCP check ===")
    print(f"checked: {len(unique) - len(skipped)}, alive: {len(alive)}, dead: {len(unique) - len(skipped) - len(alive)}, skipped (UDP protocols): {len(skipped)}")
    print(f"alive by protocol: {dict(Counter(node['protocol'] for node in alive))}")
    print(f"time: {duration} s")
    built = []
    not_converted = Counter()
    for node in alive + skipped:
        try:
            outbound = build_outbound(node["link"], "NODE_" + str(len(built)))
        except Exception as error:
            not_converted[node["protocol"] + ": " + type(error).__name__ + " " + str(error)[:60]] += 1
            continue
        built.append((node, outbound))
    print("=== Outbound build ===")
    print(f"built: {len(built)}, not converted: {sum(not_converted.values())}")
    for reason, count in not_converted.most_common(15):
        print(f"  {count} x {reason}")
    started = time.time()
    good, bad = filter_valid([outbound for _, outbound in built])
    print("=== sing-box check ===")
    print(f"valid: {len(good)}, rejected: {len(bad)}, time: {round(time.time() - started)} s")
    for message, count in Counter(message[:120] for _, message in bad).most_common(10):
        print(f"  {count} x {message}")
    node_by_tag = {outbound["tag"]: node for node, outbound in built}
    pairs = [(node_by_tag[outbound["tag"]], outbound) for outbound in good]
    started = time.time()
    print("=== URL test ===", flush=True)
    passed, reasons = check_url(pairs, settings["url_test_batch_size"], settings["url_test_timeout_seconds"], settings["url_test_retries"])
    print(f"tested: {len(pairs)}, passed: {len(passed)}, failed: {len(pairs) - len(passed)}, time: {round(time.time() - started)} s")
    print(f"passed by protocol: {dict(Counter(node['protocol'] for node in passed))}")
    for reason, count in reasons.most_common(10):
        print(f"  {count} x {reason}")
    passed_ids = {id(node) for node in passed}
    passed_pairs = [(node, outbound) for node, outbound in pairs if id(node) in passed_ids]
    started = time.time()
    print("=== Speed test ===", flush=True)
    tested = len(passed_pairs)
    passed_pairs, speed_reasons, speeds = check_speed(passed_pairs, settings["url_test_batch_size"], settings["speed_download_bytes"], settings["speed_timeout_seconds"], settings["speed_parallel"], settings["speed_min_mbps"])
    passed = [node for node, _ in passed_pairs]
    print(f"tested: {tested}, passed: {len(passed_pairs)}, time: {round(time.time() - started)} s")
    print(f"downloads completed: {len(speeds)}, at least Mbit/s: {dict((limit, sum(1 for speed in speeds if speed >= limit)) for limit in (0.5, 1, 2, 5, 10, 20))}")
    for reason, count in speed_reasons.most_common(10):
        print(f"  {count} x {reason}")
    started = time.time()
    print("=== Country detection ===", flush=True)
    services_used = detect_countries(passed_pairs, settings["url_test_batch_size"], settings["geo_timeout_seconds"])
    countries = Counter(node.get("country") or "unknown" for node in passed)
    print(f"time: {round(time.time() - started)} s")
    print(f"countries: {dict(countries.most_common(15))}")
    print(f"answered by: {dict(services_used)}")
    before = len(passed)
    passed = [node for node in passed if node.get("country") != "RU"]
    print(f"removed servers with exit in RU: {before - len(passed)}")
    lines = render(passed)
    previous_count = count_published(settings["published_url"])
    ok, message = validate(lines, previous_count, settings["min_servers"], settings["minimum_results_ratio"])
    print("=== Publish ===")
    print(f"new: {len(lines)}, previous: {previous_count}")
    if not ok:
        print("REJECTED: " + message)
        sys.exit(1)
    write_output(lines, ROOT, "XinZinVPN_Servers.txt")
    print("written XinZinVPN_Servers.txt")
main()
