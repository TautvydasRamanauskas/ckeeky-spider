## Description

Because python is single threaded, multiple instances of python were used. Application consist of:

- MySQL server, where we save url information
- Redis list, for url crawling scheduling
- Multiple python workers, which does page fetching and link discovery
- Scheduler, which takes uncrawled urls from database and adds them to Redis
- Web api, used to start crawling of new seed
- _Fake S3_, page content is saved using mock S3 and not persisted

To run the solution just use `docker-compose -f compose.yml up`. All instances should start up and if there are
uncrawled urls, crawling will start. If there is no urls to crawl, you could
use `POST http://localhost:8000/crawl {url: 'url-seed'}`. If we want to increase number of workers, we can do that by
changing `replicas` value in `compose.yml`. To check information of the crawl, you can query `page` table in MySQL.
Credentials to do that, can be found in `compose.yml`. To limit the scope of the crawl, only same-domain links are
crawled.

## Issues and possible improvements

- **Politeness** - Right now we are ignoring `robots.txt`.
- **Spider traps** - Some detections for spider traps is necessary.
- **Redirects** - Redirects are not handled and redirected pages are just ignored.
- **Sitemaps** - By using sitemaps, we could avoid manually crawling domain and instantly get all links.
- **Javascript** - Modern web uses JS a lot of, and because of that, we may be missing some elements. To crawl better we
  could use Node with Protractor, so we could fully render pages.
- **Security** - We are using raw SQL queries which are prone to SQL injection and are unsafe. Passwords are saved in
  code and Git repository is public.
- **Multiple IPs** - When crawling you are risking of getting blacklisted. If we used different trusted IPs for workers,
  this issue could be mitigated.
- **Availability** - If container crashes, there is no recovery mechanism. We could use RedisCluster and Kubernetes to
  manage instances.
- **Transactions** - If application crashes in some places, data could get corrupted and some pages will not be crawled
  properly.
- **Non HTML pages** - Not all crawled pages are `HTML`. Other types of content should be handled differently.
- **async** - Right now most of the worker time is spend on page fetch. If `async` would be used, workers could do some
  other work during that.
