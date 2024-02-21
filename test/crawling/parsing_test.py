import unittest

from crawling import parsing


class ParseLinksTest(unittest.TestCase):
    def test_no_links(self):
        links = parsing.parse_links(b'<html></html>')
        self.assertEqual(list(links), [])

    def test_multiple_links(self):
        links = parsing.parse_links(b'<html><a href="one">One</a><p>Three</p><a href="two">Two</a></html>')
        self.assertEqual(list(links), ["one", "two"])

    def test_broken_link(self):
        links = parsing.parse_links(b'<html><a>One</a></html>')
        self.assertEqual(list(links), [])
