import unittest
import json
from crawler import Crawler

class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
        self.test_url_01 = "https://www.dornheim-medical-images.de/"
        self.test_results_01 = "result_01.json"

    def test_find_all_links(self):
        self.crawler.run(self.test_url_01)
        result = self.crawler.get_results()
        with open(self.test_results_01, "r") as file:
            test_result_01 = json.load(file)
        self.assertDictEqual(result, test_result_01)

if __name__ == "__main__":
    unittest.main()