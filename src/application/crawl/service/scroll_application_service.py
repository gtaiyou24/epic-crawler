import re
import time
from typing import Optional

from injector import inject, singleton
from slf4py import set_logger

from domain.model.browser import Browser
from domain.model.url import URL, URLRepository


@singleton
@set_logger
class ScrollApplicationService:
    @inject
    def __init__(self, browser: Browser, url_repository: URLRepository):
        self.__browser = browser
        self.__url_repository = url_repository

    def crawl(self, a_seed_url: str, a_regex_to_save: str, more_selector: Optional[str]):
        seed_url = URL(a_seed_url)
        regex_to_save = re.compile(a_regex_to_save)

        self.__browser.browse(seed_url)
        while True:
            self.__browser.scroll()

            time.sleep(10.0)

            page = self.__browser.download_page()
            self.log.debug(f'URL : {page.url.absolute}')
            urls = page.get_urls()
            for detail_url in urls.filter_by_regex(regex_to_save).set:
                extracted_detail_url = detail_url.extract(regex_to_save)
                if extracted_detail_url is None:
                    self.log.warning("抽出したURLがNoneです。(detail_url={})".format(detail_url))
                self.__url_repository.save(extracted_detail_url)

            if more_selector is None:
                continue

            if not self.__browser.exist(more_selector):
                self.log.debug("次の要素が見つかりませんでした")
                break

            self.log.debug("次の要素が見つかりました")
            self.__browser.click(more_selector)
            self.log.debug("クリック！")

        self.log.debug("クロールを終了します")
