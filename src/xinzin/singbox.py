import json
import os
import subprocess
import tempfile


def base_config(outbounds):
    return {
        "log": {"level": "error"},
        "dns": {
            "servers": [{"type": "udp", "tag": "dns_direct", "server": "1.1.1.1", "server_port": 53}],
            "final": "dns_direct",
        },
        "inbounds": [],
        "outbounds": outbounds + [{"type": "direct", "tag": "direct"}],
        "route": {
            "default_domain_resolver": {"server": "dns_direct", "strategy": "ipv4_only"},
            "rules": [],
            "final": "direct",
        },
    }


def run_check(config):
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
        json.dump(config, handle)
        path = handle.name
    try:
        result = subprocess.run(["sing-box", "check", "-c", path], capture_output=True, text=True, timeout=120)
    finally:
        os.remove(path)
    return result.returncode == 0, (result.stderr or result.stdout).strip()


def filter_valid(outbounds):
    if not outbounds:
        return [], []
    ok, message = run_check(base_config(outbounds))
    if ok:
        return outbounds, []
    if len(outbounds) == 1:
        return [], [(outbounds[0], message)]
    middle = len(outbounds) // 2
    good_left, bad_left = filter_valid(outbounds[:middle])
    good_right, bad_right = filter_valid(outbounds[middle:])
    return good_left + good_right, bad_left + bad_right
