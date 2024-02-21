from urllib.parse import urljoin, urlparse


def standardize_url(current_location: str, url: str) -> str:
    return urljoin(current_location, url)


def clean_url(url: str) -> str:
    return urljoin(url, urlparse(url).path)


def get_host(url: str) -> str:
    return urlparse(url).hostname
