import re

from injector import singleton, inject

from domain.model.browser import Browser
from domain.model.url import URL, URLRepository


@singleton
class RecursiveApplicationService:
    @inject
    def __init__(self, browser: Browser, url_repository: URLRepository):
        self.__browser = browser
        self.__url_repository = url_repository
        self.__to_crawl = set()
        self.__crawled = set()

    def crawl(self, a_seed_url: str, a_regex_to_save: str, a_regex_to_crawl: str):
        seed_url = URL(a_seed_url)
        regex_to_save = re.compile(a_regex_to_save)
        regex_to_crawl = re.compile(a_regex_to_crawl)

        self.__to_crawl.add(seed_url)

        while self.__to_crawl:
            url = self.__to_crawl.pop()

            self.__browser.browse(url)
            page = self.__browser.download_page()

            for other_url in page.get_urls().set:
                if other_url.match(regex_to_save):
                    self.__url_repository.save(other_url)

                if other_url not in self.__crawled and other_url.match(regex_to_crawl):
                    self.__to_crawl.add(other_url)

            self.__crawled.add(url)
