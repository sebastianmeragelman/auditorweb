import re
from datetime import datetime


def sanitize_name(url):
    return re.sub(r'[^a-zA-Z0-9]', '', url)


def generate_filename():
    return datetime.now().strftime("%M%H%d%m%y")


def normalize_url(url):
    url = url.strip().replace('"', '').replace("'", "")

    if not url.startswith("http"):
        url = "https://" + url.lower()

    return url
