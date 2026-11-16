import base64
import json
from urllib.parse import parse_qs, unquote, urlsplit

from parsers import split_host_port

VALID_FINGERPRINTS = {"chrome", "firefox", "edge", "safari", "360", "qq", "ios", "android", "random", "randomized"}

def fix_base64(text):
    text = text.replace("-", "+").replace("_", "/")
    return text + "=" * (-len(text) % 4)


def first(params, name, default=""):
    values = params.get(name)
    return values[0] if values else default


def is_true(value):
    return str(value).strip().lower() in ("1", "true", "yes")


def get_userinfo(parts):
    if "@" not in parts.netloc:
        return ""
    return unquote(parts.netloc.rsplit("@", 1)[0])


def build_tls(server_name, fingerprint, alpn, insecure, reality_key="", short_id=""):
    tls = {"enabled": True}

    fingerprint = fingerprint.lower()
    if fingerprint not in VALID_FINGERPRINTS:
        fingerprint = ""
    if server_name:
        tls["server_name"] = server_name
    if insecure:
        tls["insecure"] = True
    if alpn:
        tls["alpn"] = [item for item in alpn.split(",") if item]
    if fingerprint or reality_key:
        tls["utls"] = {"enabled": True, "fingerprint": fingerprint or "chrome"}
    if reality_key:
        tls["reality"] = {"enabled": True, "public_key": reality_key, "short_id": short_id}
    return tls


def build_transport(kind, path, host, service_name):
    if kind in ("", "tcp", "none", "raw"):
        return None
    if kind == "ws":
        transport = {"type": "ws", "path": path or "/"}
        if host:
            transport["headers"] = {"Host": host}
        return transport
    if kind == "grpc":
        return {"type": "grpc", "service_name": service_name}
    if kind == "httpupgrade":
        transport = {"type": "httpupgrade", "path": path or "/"}
        if host:
            transport["host"] = host
        return transport
    raise ValueError("transport " + kind)


def build_vless(link, tag):
    parts = urlsplit(link)
    params = parse_qs(parts.query)
    if not parts.hostname:
        raise ValueError("no host")
    outbound = {
        "type": "vless",
        "tag": tag,
        "server": parts.hostname,
        "server_port": parts.port,
        "uuid": get_userinfo(parts),
    }
    flow = first(params, "flow")
    if flow.endswith("-udp443"):
        flow = flow[:-7]
    if flow and flow != "none":
        outbound["flow"] = flow
    if first(params, "encryption", "none") not in ("", "none"):
        raise ValueError("vless encryption")
    security = first(params, "security", "none")
    if security in ("tls", "reality"):
        reality_key = first(params, "pbk") if security == "reality" else ""
        if security == "reality" and not reality_key:
            raise ValueError("reality without key")
        insecure = is_true(first(params, "allowInsecure")) or is_true(first(params, "insecure"))
        outbound["tls"] = build_tls(
            first(params, "sni") or first(params, "host"),
            first(params, "fp"),
            first(params, "alpn"),
            insecure,
            reality_key,
            first(params, "sid"),
        )
    elif security != "none":
        raise ValueError("security " + security)
    kind = first(params, "type", "tcp")
    if kind == "tcp" and first(params, "headerType") == "http":
        raise ValueError("tcp http header")
    transport = build_transport(kind, first(params, "path"), first(params, "host"), first(params, "serviceName") or first(params, "path"))
    if transport:
        outbound["transport"] = transport
    return outbound


def build_trojan(link, tag):
    parts = urlsplit(link)
    params = parse_qs(parts.query)
    if not parts.hostname:
        raise ValueError("no host")
    outbound = {
        "type": "trojan",
        "tag": tag,
        "server": parts.hostname,
        "server_port": parts.port,
        "password": get_userinfo(parts),
    }
    security = first(params, "security", "tls")
    if security in ("tls", ""):
        insecure = is_true(first(params, "allowInsecure")) or is_true(first(params, "insecure"))
        outbound["tls"] = build_tls(first(params, "sni") or first(params, "peer") or first(params, "host"), first(params, "fp"), first(params, "alpn"), insecure)
    elif security != "none":
        raise ValueError("security " + security)
    kind = first(params, "type", "tcp")
    if kind == "tcp" and first(params, "headerType") == "http":
        raise ValueError("tcp http header")
    transport = build_transport(kind, first(params, "path"), first(params, "host"), first(params, "serviceName") or first(params, "path"))
    if transport:
        outbound["transport"] = transport
    return outbound


def build_shadowsocks(link, tag):
    rest = link.split("://", 1)[1].split("#", 1)[0]
    main, _, query = rest.partition("?")
    if "plugin=" in query:
        raise ValueError("ss plugin")
    main = main.rstrip("/")
    if "@" in main:
        userinfo, hostport = main.rsplit("@", 1)
        if ":" in userinfo:
            userinfo = unquote(userinfo)
        else:
            userinfo = base64.b64decode(fix_base64(unquote(userinfo))).decode("utf-8")
    else:
        decoded = base64.b64decode(fix_base64(unquote(main))).decode("utf-8")
        userinfo, hostport = decoded.rsplit("@", 1)
    method, password = userinfo.split(":", 1)
    host, port = split_host_port(hostport)
    return {
        "type": "shadowsocks",
        "tag": tag,
        "server": host,
        "server_port": port,
        "method": method,
        "password": password,
    }


def build_vmess(link, tag):
    payload = link.split("://", 1)[1].split("#", 1)[0]
    data = json.loads(base64.b64decode(fix_base64(payload)).decode("utf-8", errors="replace"))
    outbound = {
        "type": "vmess",
        "tag": tag,
        "server": str(data["add"]).strip(),
        "server_port": int(data["port"]),
        "uuid": str(data["id"]).strip(),
        "alter_id": int(data.get("aid") or 0),
        "security": data.get("scy") or "auto",
    }
    host = str(data.get("host") or "")
    path = str(data.get("path") or "")
    if str(data.get("tls", "")).lower() in ("tls", "1", "true"):
        outbound["tls"] = build_tls(str(data.get("sni") or host), str(data.get("fp") or ""), str(data.get("alpn") or ""), is_true(data.get("allowInsecure", "")))
    kind = str(data.get("net") or "tcp")
    if kind == "tcp" and str(data.get("type") or "none") not in ("none", ""):
        raise ValueError("tcp http header")
    transport = build_transport(kind, path, host, path)
    if transport:
        outbound["transport"] = transport
    return outbound


def build_hysteria2(link, tag):
    parts = urlsplit("hysteria2://" + link.split("://", 1)[1])
    params = parse_qs(parts.query)
    if not parts.hostname:
        raise ValueError("no host")
    outbound = {
        "type": "hysteria2",
        "tag": tag,
        "server": parts.hostname,
        "server_port": parts.port,
        "password": get_userinfo(parts),
        "tls": build_tls(first(params, "sni"), "", first(params, "alpn"), is_true(first(params, "insecure")) or is_true(first(params, "allowInsecure"))),
    }
    obfs = first(params, "obfs")
    if obfs == "salamander":
        outbound["obfs"] = {"type": "salamander", "password": first(params, "obfs-password")}
    elif obfs and obfs != "none":
        raise ValueError("obfs " + obfs)
    return outbound


def build_tuic(link, tag):
    parts = urlsplit(link)
    params = parse_qs(parts.query)
    if not parts.hostname:
        raise ValueError("no host")
    uuid, _, password = get_userinfo(parts).partition(":")
    return {
        "type": "tuic",
        "tag": tag,
        "server": parts.hostname,
        "server_port": parts.port,
        "uuid": uuid,
        "password": password,
        "congestion_control": first(params, "congestion_control", "bbr"),
        "tls": build_tls(first(params, "sni"), "", first(params, "alpn"), is_true(first(params, "allow_insecure")) or is_true(first(params, "insecure"))),
    }


BUILDERS = {
    "vless": build_vless,
    "trojan": build_trojan,
    "ss": build_shadowsocks,
    "vmess": build_vmess,
    "hysteria2": build_hysteria2,
    "hy2": build_hysteria2,
    "tuic": build_tuic,
}


def build_outbound(link, tag):
    scheme = link.split("://", 1)[0].lower()
    builder = BUILDERS.get(scheme)
    if builder is None:
        raise ValueError("protocol " + scheme)
    return builder(link, tag)
