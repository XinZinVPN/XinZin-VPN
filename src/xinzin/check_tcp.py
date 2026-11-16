import socket
from concurrent.futures import ThreadPoolExecutor

UDP_PROTOCOLS = {"hysteria", "hysteria2", "tuic"}


def check_one(node, timeout):
    try:
        with socket.create_connection((node["address"], node["port"]), timeout=timeout):
            return True
    except Exception:
        return False


def check_tcp(nodes, timeout, parallel):
    to_check = [node for node in nodes if node["protocol"] not in UDP_PROTOCOLS]
    skipped = [node for node in nodes if node["protocol"] in UDP_PROTOCOLS]
    with ThreadPoolExecutor(max_workers=parallel) as pool:
        results = list(pool.map(lambda node: check_one(node, timeout), to_check))
    alive = [node for node, ok in zip(to_check, results) if ok]
    return alive, skipped
