from uuid import uuid4

import mysql.connector

COLUMN_ID = 0
COLUMN_URL = 1
COLUMN_CRAWL_ATTEMPTS = 3

DATABASE = mysql.connector.connect(
    host="host.docker.internal",
    # host="localhost",
    port=33060,
    user="crawler",
    passwd="3YMPamyXo!@B",
    database="spider"
)
DATABASE.autocommit = True


def add_page_to_crawl(url: str) -> None:
    uuid = uuid4()
    query = f"INSERT IGNORE INTO page (id,url) VALUES ('{uuid}','{url}')"
    cursor = DATABASE.cursor()
    cursor.execute(query)


def add_crawled_page(url: str, file_location: str) -> None:
    query = f"UPDATE page SET file_location = '''{file_location}''', crawl_timestamp = UTC_TIMESTAMP() WHERE url = '{url}'"
    cursor = DATABASE.cursor()
    cursor.execute(query)


def get_pages_to_crawl(limit=100) -> list[tuple]:
    query = f"SELECT * FROM page WHERE file_location IS NULL AND crawl_attempts = 0 LIMIT {limit}"
    cursor = DATABASE.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def increase_crawl_count(pages: list[tuple]) -> None:
    if not pages:
        return

    values = (f"('{page[COLUMN_ID]}', '{page[COLUMN_URL]}', {page[COLUMN_CRAWL_ATTEMPTS] + 1})" for page in pages)
    query = (f"INSERT into `page` (id, url, crawl_attempts) "
             f"VALUES {", ".join(values)} "
             f"ON DUPLICATE KEY UPDATE crawl_attempts = VALUES(crawl_attempts)")
    cursor = DATABASE.cursor()
    cursor.execute(query)
