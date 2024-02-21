from fastapi import FastAPI
from pydantic import BaseModel

from external import redis_queue, pages as pages_service

APP = FastAPI()


class CrawlRequest(BaseModel):
    url: str


@APP.post("/crawl")
async def read_root(request: CrawlRequest) -> None:
    print(f"Starting crawling of url - {request.url}")
    pages_service.add_page_to_crawl(request.url)
    redis_queue.push(request.url)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(APP, host="127.0.0.1", port=8000)
