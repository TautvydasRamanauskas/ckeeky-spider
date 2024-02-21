from typing import Generator

from bs4 import BeautifulSoup


def parse_links(content: bytes) -> Generator[str, None, None]:
    soup = BeautifulSoup(content, features="html.parser")
    for element in soup.findAll("a"):
        try:
            yield element["href"]
        except KeyError:
            pass
