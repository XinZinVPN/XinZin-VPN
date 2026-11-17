import urllib.request


def count_published(url):
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "XinZinVPN"})
        with urllib.request.urlopen(request, timeout=30) as response:
            text = response.read().decode("utf-8", errors="replace")
    except Exception:
        return None
    return len([line for line in text.splitlines() if "://" in line])


def validate(lines, previous_count, min_servers, min_ratio):
    if len(lines) < min_servers:
        return False, "only " + str(len(lines)) + " servers, minimum is " + str(min_servers)
    if previous_count and len(lines) < previous_count * min_ratio:
        return False, "new list has " + str(len(lines)) + " servers, previous had " + str(previous_count)
    for line in lines:
        if "://" not in line:
            return False, "bad line: " + line[:60]
    return True, ""


def write_output(lines, directory, filename):
    directory.mkdir(parents=True, exist_ok=True)
    temp = directory / (filename + ".tmp")
    temp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    temp.replace(directory / filename)
