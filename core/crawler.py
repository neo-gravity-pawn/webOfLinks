from bs4 import BeautifulSoup
from urllib import request, parse
import urllib.error

class Crawler:
    def __init__(self):
        self.results = dict()
        self.max_nr_iterations = -1
        self.nr_interations = 0
        self.domain = ""
        self.ignore_internal_query_urls = True 
    
    def run(self, url):
        parsed_url = parse.urlparse(url)
        self.domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        print(self.domain)
        self.results[url] = {"to": url, "is_external": False, "is_file": False}
        self.__parse_url(self.results[url])

    def get_results(self):
        return self.results
    
    def __parse_url(self, info):
        url = info["to"]
        status = 0
        count_hint = f"/{self.max_nr_iterations}" if self.max_nr_iterations != -1 else ""
        print(f"Parse({self.nr_interations}{count_hint}): {url}")
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3"}
        req = request.Request(url=url, headers=headers) 
        try:
            response = request.urlopen(req)
        except urllib.error.HTTPError:
            status = 404
        except:
            print("URL OPEN: unexpected error")
            status = 666
        status = response.status if status == 0 else status
        self.__set_status(url, status) 
        if self.__is_ok_to_be_parsed(url):
            url_links = self.__extract_links(url, response)
            for link in url_links:
                self.nr_interations += 1
                if self.max_nr_iterations > 0 and self.nr_interations > self.max_nr_iterations:
                    break
                if not self.results[link["to"]]["visited"]:
                    self.__parse_url(link)
    
    def __set_status(self, url, status):
        if url in self.results:
            self.results[url]["status"] = status
            self.results[url]["visited"] = True

    def __is_ok_to_be_parsed(self, url):
        info = self.results[url]
        return \
        not (self.ignore_internal_query_urls and self.__is_internal_query_url(url)) and \
        not info["is_file"] and \
        not info["is_external"] and \
        info["status"] == 200 

    def __is_external_url(self, url):
        return not url.startswith(self.domain) and url.startswith("http")

    def __is_internal_query_url(self, url):
        parsed_url = parse.urlparse(url)
        return not self.results[url]["is_external"] and parsed_url.query != ""
        
    def __extract_links(self, url, response):
        links_for_current_url = []
        soup = BeautifulSoup(response, "lxml", from_encoding=response.info().get_param("charset"))
        for link in soup.find_all("a", href=True):
            process_result = self.__process_link(url, link["href"])
            if process_result:
                links_for_current_url.append(process_result)
        return links_for_current_url

    def __process_link(self, base_url, url):
        is_external = not url.startswith(self.domain) and url.startswith("http")
        is_file = self.__is_probably_file(url)
        if not is_external:
            url = self.__convert_to_absolute_url(url)
        if not url in self.results:
            self.results[url] = {
                "from": base_url, 
                "to": url, 
                "is_external": is_external, 
                "status": 0, 
                "is_file": is_file, 
                "visited": False }
            return self.results[url]
        return None
    
    def __is_probably_file(self, url):
        ok_extensions = ["html", "htm", "php"]
        slash_segments = url.split("/")
        dot_segments = slash_segments[-1].split(".")
        ext = dot_segments[-1]
        return len(dot_segments) > 1 and not ext in ok_extensions

    def __convert_to_absolute_url(self, url):
        return parse.urljoin(self.domain, url) if not url.startswith("http") else url