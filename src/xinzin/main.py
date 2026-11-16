import base64
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def download(url):
    request = urllib.request.Request(url, headers={"User-Agent": "XinZinVPN"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def decode_if_base64(text):
    if "://" in text:
        return text, False
    try:
        compact = "".join(text.split())
        compact += "=" * (-len(compact) % 4)
        decoded = base64.b64decode(compact).decode("utf-8", errors="replace")
        return decoded, True
    except Exception:
        return text, False


def scheme_of(line):
    if "://" not in line:
        return "other"
    return line.split("://", 1)[0].lower()


def main():
    config_path = ROOT / "config" / "sources.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    total = 0
    print("=== XinZinVPN: source report ===")
    for source in config["sources"]:
        name = source["name"]
        try:
            text = download(source["url"])
        except Exception as error:
            print(f"[FAIL] {name}: {error}")
            continue
        text, was_base64 = decode_if_base64(text)
        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        schemes = Counter(scheme_of(line) for line in lines)
        total += len(lines)
        base64_note = " (base64)" if was_base64 else ""
        print(f"[OK] {name}: {len(lines)} lines{base64_note} -> {dict(schemes)}")
    print(f"=== total lines: {total} ===")


main()
