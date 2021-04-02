from bs4 import BeautifulSoup
from urllib import request, parse
import urllib.error

class Crawler:
    def __init__(self):
        self.results = dict()
        self.max_nr_iterations = -1
        self.nr_interations = 0
        self.domain = ''

    def set_max_nr_of_interations(self, max_nr):
        self.max_nr_iterations = max_nr
    
    def run(self, url):
        parsed_url = parse.urlparse(url)
        self.domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        self.__parse_url({'url': url, 'is_external': False, 'is_file': False})

    def get_results(self):
        return self.results
    
    def __parse_url(self, info):
        status = 0
        print("Parse: ", info["url"])
        try:
            response = request.urlopen(info["url"])
        except urllib.error.HTTPError:
            status = 404
        status = response.status if status == 0 else status
        self.__set_status(info["url"], status) 
        if not info["is_external"] and not info["is_file"] and status == 200:
            url_links = self.__parse_for_links(info["url"], response)
            for link in url_links:
                self.nr_interations += 1
                if self.max_nr_iterations > 0 and self.nr_interations > self.max_nr_iterations:
                    break
                if not self.results[link["url"]]["visited"]:
                    self.__parse_url(link)
    
    def __set_status(self, url, status):
        if url in self.results:
            self.results[url]["status"] = status
            self.results[url]["visited"] = True

    def __parse_for_links(self, url, response):
        links_for_current_url = []
        soup = BeautifulSoup(response, 'lxml', from_encoding=response.info().get_param('charset'))
        for link in soup.find_all('a', href=True):
            processed_url, is_external, is_file = self.__process_link(url, link['href'])
            if processed_url is not None:
                links_for_current_url.append({"url": processed_url, "is_external": is_external, "is_file": is_file})
        return links_for_current_url

    def __process_link(self, base_url, url):
        if not self.__is_no_link(url):
            is_external = not url.startswith(self.domain) and url.startswith('http')
            is_file = self.__is_download_link(url)
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
                return url, is_external, is_file
        return None, None, None
    
    def __is_no_link(self, url):
        return self.__start_or_ends_with(url, ['mailto:', 'javascript:'])

    
    def __is_download_link(self, url):
        return self.__start_or_ends_with(url, ['.msi', '.pkg', '.rpm', '.deb', '.zip', '.exe', '.pdf'])

    def __start_or_ends_with(self, term, list):
        for entry in list:
            if term.startswith(entry) or term.endswith(entry):
                return True
        return False

    def __convert_to_absolute_url(self, url):
        return parse.urljoin(self.domain, url) if not url.startswith('http') else url