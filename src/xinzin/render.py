import base64
import json
from urllib.parse import quote

from geo import flag
from outbounds import fix_base64


def clean_link(link):
    base = link.split("#", 1)[0]
    if base.lower().startswith("hy2://"):
        base = "hysteria2://" + base[6:]
    head, mark, query = base.partition("?")
    if not mark:
        return base
    parts = [part for part in query.split("&") if part]
    return head + "?" + "&".join(parts) if parts else head


def rename_link(link, name):
    scheme = link.split("://", 1)[0].lower()
    if scheme == "vmess":
        payload = link.split("://", 1)[1].split("#", 1)[0]
        data = json.loads(base64.b64decode(fix_base64(payload)).decode("utf-8", errors="replace"))
        data = {key: value for key, value in data.items() if value is not None and key not in ("name", "test_name")}
        data["v"] = "2"
        data["ps"] = name
        encoded = base64.b64encode(json.dumps(data, ensure_ascii=False).encode("utf-8")).decode("ascii")
        return "vmess://" + encoded
    return clean_link(link) + "#" + quote(name)


def sort_key(node):
    country = node.get("country") or ""
    return (country == "", country, node.get("latency", 99))


def render(nodes):
    lines = []
    for node in sorted(nodes, key=sort_key):
        name = flag(node.get("country")) + " XinZinVPN"
        try:
            lines.append(rename_link(node["link"], name))
        except Exception:
            continue
    return lines
