import unittest
import json
from renderer import Renderer

class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.renderer = Renderer()
        self.test_input_01 = "result_dornheim_10.json"
        self.test_result_01 = "result_dornheim_10.html"
        

    def test_rendering(self):
        test_output = "test_result.html"
        with open(self.test_input_01, "r") as file:
            test_input_01 = json.load(file)
        self.renderer.render_json_result(test_input_01, test_output)
        with open(self.test_result_01, 'r') as file:
            test_data = file.read()
            with open(test_output) as file2:
                test_output = file2.read()
                self.assertEqual(test_data, test_output)
                

if __name__ == "__main__":
    unittest.main()