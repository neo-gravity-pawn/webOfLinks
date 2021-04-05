import unittest
import json
# pylint: disable=import-error
from core.crawler import Crawler


class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.crawler = Crawler()
        self.test_url_01 = "https://dornheim.tech"
        self.test_results_01 = "test/test_data/result_dornheim_10.json"

    def test_find_all_links(self):
        self.crawler.max_nr_iterations = 10
        self.crawler.run(self.test_url_01)
        result = self.crawler.get_results()
        #with open(self.test_results_01, "w") as file:
        #    json.dump(result, file)
        with open(self.test_results_01, "r") as file:
            test_result_01 = json.load(file)
        self.assertDictEqual(result, test_result_01)

if __name__ == "__main__":
    unittest.main()