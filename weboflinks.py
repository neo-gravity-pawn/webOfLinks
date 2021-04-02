import sys
import json
# pylint: disable=import-error
from core.crawler import Crawler
from core.renderer import Renderer

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        print("at least 2 arguments expected: [url] [result_id] [max_nr_of_links: optional]")
    else:
        crawler = Crawler()
        print(f"Crawling {args[1]}..."),
        if len(args) == 4:
            print(f"stopping when more than {args[3]} links are found...")
            crawler.set_max_nr_of_interations(int(args[3]))
        crawler.run(args[1])
        json_file_path = f"results/{args[2]}.json"
        result = crawler.get_results()
        with open(json_file_path, "w") as file:
            json.dump(result, file)
        print(f"Crawling result saved to {json_file_path}")
        print(f"Render link network..."),
        renderer = Renderer()
        html_file_path = f"results/{args[2]}.html"
        renderer.render_json_result(result, html_file_path)
        print(f"saved to {html_file_path}")