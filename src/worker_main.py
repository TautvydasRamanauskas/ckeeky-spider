from external import redis_queue
from crawling import crawler


def main() -> None:
    _crawl()


def _crawl() -> None:
    for url in redis_queue.subscribe():
        _crawl_page(url)


def _crawl_page(url: str) -> None:
    try:
        page_crawler = crawler.Crawler(url)
        page_crawler.crawl()
    except Exception as e:
        print(f"Error occurred while trying to crawl url {url} - {e}")


if __name__ == "__main__":
    main()
