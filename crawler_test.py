import unittest
from crawler import Crawler

class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()

    def test_find_all_links(self):
        test_url = 'https://www.crawler-test.com/links/broken_links_internal'
        self.crawler.set_start_url(test_url)
        self.crawler.run()
        res = self.crawler.get_results()
        print(res)

        self.assertEqual('foo'.lower(), 'FOO')


if __name__ == '__main__':
    unittest.main()