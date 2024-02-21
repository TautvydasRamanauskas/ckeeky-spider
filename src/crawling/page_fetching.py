import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
}
TIMEOUT = 30


def fetch_page(url: str) -> bytes:
    response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    if response.status_code == 200:
        return response.content
    raise ConnectionError(f"Failed to fetch url - {url} with status code - {response.status_code}")
