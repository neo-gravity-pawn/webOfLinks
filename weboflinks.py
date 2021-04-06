import sys
import json
import argparse
# pylint: disable=import-error
from core.crawler import Crawler
from core.renderer import Renderer

def crawl(args):
    crawler = Crawler()
    print(f"Crawling {args.url}...")
    if args.max:
        print(f"- stopping when more than {args.max} links are found...")
        crawler.max_nr_iterations = int(args.max)
    if args.noquery:
        print("- ignoring internal links with query parameters...")
        crawler.ignore_internal_query_urls = True
    crawler.run(args.url)
    json_file_path = f"results/{args.out}.json"
    result = crawler.get_results()
    with open(json_file_path, "w") as file:
        json.dump(result, file)
    print(f"...crawling result saved to {json_file_path}")
    return result

def render(args, result):
    print(f"Render link network..."),
    renderer = Renderer()
    html_file_path = f"results/{args.out}.html"
    renderer.render_json_result(result, html_file_path)
    print(f"...saved to {html_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser._action_groups.pop()

    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument("--url", help="url that should be parsed",required=True)
    required.add_argument("--out", help="unique name for the generated output files",required=True)
    optional.add_argument("--max", help="maximum number of links that should be parsed")
    optional.add_argument("--noquery", help="local links with querys won't be parsed", action="store_true")

    args = parser.parse_args()
    result = crawl(args)
    render(args, result)


# TODO
# FUTURE IMPROVEMENTS
#   FULL GRAPH
#   BETTER HANDLING OF DYNAMIC CONTENT (CALENDAR)
#   ...