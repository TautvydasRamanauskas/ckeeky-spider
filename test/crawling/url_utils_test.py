import unittest

from crawling import url_utils

TEST_URL = "https://blog.spider.com/page-a"


class StandardizeUrlTest(unittest.TestCase):
    def test_relative(self):
        url = url_utils.standardize_url(TEST_URL, "subpage-a")
        self.assertEqual("https://blog.spider.com/subpage-a", url)

    def test_root_relative(self):
        url = url_utils.standardize_url(TEST_URL, "/page-b")
        self.assertEqual("https://blog.spider.com/page-b", url)

    def test_absolute(self):
        url = url_utils.standardize_url(TEST_URL, "https://blog.spider.com/page-c")
        self.assertEqual("https://blog.spider.com/page-c", url)

    def test_absolute_no_protocol(self):
        url = url_utils.standardize_url(TEST_URL, "//blog.spider.com/page-d")
        self.assertEqual("https://blog.spider.com/page-d", url)

    def test_section_url(self):
        url = url_utils.standardize_url(TEST_URL, "#section-a")
        self.assertEqual("https://blog.spider.com/page-a#section-a", url)


class CleanUrlTest(unittest.TestCase):
    def test_cleans_query_params(self):
        url = url_utils.clean_url(TEST_URL + "?q=a&f=2")
        self.assertEqual("https://blog.spider.com/page-a", url)

    def test_cleans_section_id(self):
        url = url_utils.clean_url(TEST_URL + "#section-a")
        self.assertEqual("https://blog.spider.com/page-a", url)


class GetHostTest(unittest.TestCase):
    def test_get_host(self):
        url = url_utils.get_host("https://blog.spider.com/page-a/subpage-a#section-a?q=1&f=3")
        self.assertEqual("blog.spider.com", url)
