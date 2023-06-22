from dataclasses import dataclass

from domain.model.page import HttpStatus
from domain.model.page.html import HTML
from domain.model.url import URL, URLSet


@dataclass(init=False, unsafe_hash=True, frozen=True)
class Page:
    url: URL
    http_status: HttpStatus
    html: HTML

    def __init__(self, url: URL, http_status: HttpStatus, html: HTML):
        assert url, "URLは必須です"
        assert http_status, "HTTPステータスは必須です"
        assert html, "HTMLは必須です"
        super().__setattr__("url", url)
        super().__setattr__("http_status", http_status)
        super().__setattr__("html", html)

    def get_urls(self) -> URLSet:
        return self.html.urls(self.url)
