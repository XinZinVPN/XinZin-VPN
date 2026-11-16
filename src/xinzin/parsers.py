import base64
import json
from urllib.parse import urlsplit


def fix_base64(text):
    text = text.replace("-", "+").replace("_", "/")
    return text + "=" * (-len(text) % 4)


def split_host_port(hostport):
    hostport = hostport.strip().strip("/")
    if hostport.startswith("["):
        host, _, port = hostport[1:].partition("]:")
    else:
        host, _, port = hostport.rpartition(":")
    return host, int(port)


def parse_vmess(link):
    payload = link.split("://", 1)[1].split("#", 1)[0]
    data = json.loads(base64.b64decode(fix_base64(payload)).decode("utf-8", errors="replace"))
    return str(data["add"]).strip(), int(data["port"])


def parse_shadowsocks(link):
    rest = link.split("://", 1)[1].split("#", 1)[0].split("?", 1)[0]
    if "@" in rest:
        return split_host_port(rest.rsplit("@", 1)[1])
    decoded = base64.b64decode(fix_base64(rest)).decode("utf-8", errors="replace")
    return split_host_port(decoded.rsplit("@", 1)[1])


def parse_link(link):
    scheme = link.split("://", 1)[0].lower()
    if scheme == "hy2":
        scheme = "hysteria2"
    try:
        if scheme == "vmess":
            host, port = parse_vmess(link)
        elif scheme == "ss":
            host, port = parse_shadowsocks(link)
        else:
            parts = urlsplit(link)
            host, port = parts.hostname, parts.port
        if not host or not port:
            return None
        return {"protocol": scheme, "address": host.lower(), "port": port, "link": link}
    except Exception:
        return None
