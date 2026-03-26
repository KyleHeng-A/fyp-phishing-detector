import re


def analyze_url(url):
    features = {
        "uses_ip_address": bool(re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url)),
        "shortened_url": any(service in url for service in ["bit.ly", "tinyurl", "goo.gl"]),
        "many_subdomains": url.count(".") > 4,
        "not_https": not url.startswith("https://")
    }

    return features
