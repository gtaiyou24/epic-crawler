import re
from typing import Set

from injector import inject, singleton
from slf4py import set_logger

from domain.model.page import PageService
from domain.model.url import URL, URLRepository


@singleton
@set_logger
class PaginationApplicationService:
    @inject
    def __init__(self, page_service: PageService, url_repository: URLRepository):
        self.__page_service = page_service
        self.__url_repository = url_repository
        self.__to_crawl: Set[URL] = set()
        self.__crawled = set()

    def crawl(self, an_index_url: str, an_index_url_regex: str, a_detail_url_regex: str):
        index_url = URL(an_index_url)
        index_url_regex = re.compile(an_index_url_regex)
        detail_url_regex = re.compile(a_detail_url_regex)

        self.__to_crawl.add(index_url)

        while self.__to_crawl:
            self.log.debug("to crawl : {}".format(len(self.__to_crawl)))
            index_url = self.__to_crawl.pop()
            index_page = self.__page_service.download(index_url)

            # 詳細ページのURLを保存
            urls = index_page.get_urls()
            for detail_url in urls.filter_by_regex(detail_url_regex).set:
                self.log.debug("詳細ページURL : {}".format(detail_url))
                self.__url_repository.save(detail_url)

            # 一覧ページのURLを保存
            for other_index_url in urls.filter_by_regex(index_url_regex).set:
                if other_index_url not in self.__crawled:
                    self.log.debug("一覧ページURL : {}".format(other_index_url))
                    self.__to_crawl.add(other_index_url)
