from time import sleep
from typing import Iterator

import redis

TIMEOUT = 30
# CLIENT = redis.Redis(host='localhost', port=6382, decode_responses=True)
CLIENT = redis.Redis(host='host.docker.internal', port=6382, decode_responses=True, socket_timeout=TIMEOUT)
LIST_NAME = "url-list"


def push(url: str) -> None:
    CLIENT.rpush(LIST_NAME, url)


def subscribe() -> Iterator[str]:
    while True:
        urls = CLIENT.lpop(LIST_NAME, 1)
        if urls:
            print(f"Received url: {urls}")
            yield from urls
        else:
            sleep(1)


def get_length() -> int:
    return CLIENT.llen(LIST_NAME)
