import unittest

from crawling import page_fetching


class FetchPageTest(unittest.TestCase):
    def test_fetch_page_success(self):
        page = page_fetching.fetch_page("https://en.wikipedia.org/")
        self.assertIsNotNone(page)

    def test_fetch_page_fail(self):
        with self.assertRaises(ConnectionError):
            page_fetching.fetch_page("https://en.wikipedia.org/admin")
