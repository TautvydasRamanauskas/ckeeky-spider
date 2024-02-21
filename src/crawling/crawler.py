from typing import Iterator
import hashlib

from external import pages as pages_service, s3 as s3_service
from crawling import parsing, page_fetching, url_utils

STAY_IN_HOST = True


class Crawler:
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.host = url_utils.get_host(url)

    def crawl(self) -> None:
        page = page_fetching.fetch_page(self.url)
        links = set(self._find_links(page))
        print(f'Discovered {len(links)} while crawling url {self.url}')
        for link in links:
            pages_service.add_page_to_crawl(link)

        filename = self._get_s3_location()
        s3_service.S3.upload_file(filename, page)
        pages_service.add_crawled_page(self.url, filename)

    def _find_links(self, page_content: bytes) -> Iterator[str]:
        links = parsing.parse_links(page_content)
        for link in links:
            standardized_url = url_utils.standardize_url(self.url, link)
            cleaned_url = url_utils.clean_url(standardized_url)
            if self._is_supported_link(cleaned_url):
                yield cleaned_url

    def _is_supported_link(self, link: str) -> bool:
        return not STAY_IN_HOST or url_utils.get_host(link) == self.host

    def _get_s3_location(self) -> str:
        h = hashlib.new('sha256')
        h.update(self.url.encode())
        return f"/pages/{h.hexdigest()}"
