from bs4 import BeautifulSoup
from urllib import request, parse

class Crawler:
    def __init__(self):
        self.results = dict()

    def set_start_url(self, url):
        self.start_url = url
    
    def run(self):
        response = request.urlopen(self.start_url)
        self.__parse_for_links(self.start_url, response)

    def get_results(self):
        return self.results
    
    def __parse_for_links(self, url, response):
        soup = BeautifulSoup(response, 'html.parser')
        status = response.status
        for link in soup.find_all('a', href=True):
            self.__process_link(url, link['href'])

    def __process_link(self, base_url, url):
        is_external = url.startswith('http')
        if not is_external:
            url = self.__convert_to_absolute_url(base_url, url)
        already_discoverd = url in self.results
        if not already_discoverd:
            self.results[url] = {"from": base_url, "to": url, "is_external": is_external, "status": 0}
        return self.results[url]
    
    def __convert_to_absolute_url(self, base_url, url):
        return parse.urljoin(base_url, url) if not url.startswith(base_url) else url
