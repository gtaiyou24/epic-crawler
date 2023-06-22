import requests

from domain.model.page import PageService, Page, HttpStatus
from domain.model.page.html import HTML, CharacterCode
from domain.model.url import URL


class SyncPageService(PageService):
    def __init__(self):
        super().__init__()

    def _download(self, url: URL, connect_timeout: float, read_timeout: float) -> Page:
        page_url = URL(url.absolute)
        response = requests.get(url.absolute, timeout=(self.__connect_timeout, self.__read_timeout))
        http_status = HttpStatus.value_of(response.status_code)
        html = HTML(response.text, CharacterCode.value_of(response.apparent_encoding))
        return Page(page_url, http_status, html)
