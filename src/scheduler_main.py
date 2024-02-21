from time import sleep

from external import pages as pages_service, redis_queue

SCHEDULE_INTERVAL = 10
MAX_LIMIT = 100


def main() -> None:
    _schedule()


def _schedule() -> None:
    while True:
        limit = MAX_LIMIT - redis_queue.get_length()
        pages_to_crawl = pages_service.get_pages_to_crawl(limit)
        if pages_to_crawl:
            pages_service.increase_crawl_count(pages_to_crawl)
            urls_to_crawl = [p[pages_service.COLUMN_URL] for p in pages_to_crawl]

            print(f"Scheduling {len(urls_to_crawl)} urls for crawling")
            for url in urls_to_crawl:
                redis_queue.push(url)

        sleep(SCHEDULE_INTERVAL)


if __name__ == "__main__":
    main()
