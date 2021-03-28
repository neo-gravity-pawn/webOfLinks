import unittest
import json
from crawler import Crawler

class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
        self.test_data_01 = '{"https://www.crawler-test.com/": {"from": "https://www.crawler-test.com/links/broken_links_internal", "to": "https://www.crawler-test.com/", "is_external": false, "status": 0}, "https://www.crawler-test.com/links/not_found/foo1": {"from": "https://www.crawler-test.com/links/broken_links_internal", "to": "https://www.crawler-test.com/links/not_found/foo1", "is_external": false, "status": 0}, "https://www.crawler-test.com/links/not_found/foo2": {"from": "https://www.crawler-test.com/links/broken_links_internal", "to": "https://www.crawler-test.com/links/not_found/foo2", "is_external": false, "status": 0}, "https://www.crawler-test.com/links/not_found/foo3": {"from": "https://www.crawler-test.com/links/broken_links_internal", "to": "https://www.crawler-test.com/links/not_found/foo3", "is_external": false, "status": 0}, "https://www.crawler-test.com/links/not_found/foo4": {"from": "https://www.crawler-test.com/links/broken_links_internal", "to": "https://www.crawler-test.com/links/not_found/foo4", "is_external": false, "status": 0}, "https://www.crawler-test.com/links/not_found/foo5": {"from": "https://www.crawler-test.com/links/broken_links_internal", "to": "https://www.crawler-test.com/links/not_found/foo5", "is_external": false, "status": 0}}'

    def test_find_all_links(self):
        test_url = 'https://www.crawler-test.com/links/broken_links_internal'
        self.crawler.set_start_url(test_url)
        self.crawler.run()
        res = self.crawler.get_results()
        print(json.dumps(res))
        self.assertDictEqual(res, json.loads(self.test_data_01))


if __name__ == '__main__':
    unittest.main()