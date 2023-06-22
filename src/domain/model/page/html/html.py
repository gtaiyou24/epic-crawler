from dataclasses import dataclass

from bs4 import BeautifulSoup

from domain.model.page.html import CharacterCode
from domain.model.url import URL, URLSet


@dataclass(init=False, unsafe_hash=True, frozen=True)
class HTML:
    text: str
    character_code: CharacterCode

    def __init__(self, text: str, character_code: CharacterCode):
        super().__setattr__("text", text)
        super().__setattr__("character_code", character_code)

    def is_not_empty(self) -> bool:
        return self.text is not None and self.text != ''

    def urls(self, base_url: URL) -> URLSet:
        if self.text is None:
            return URLSet(set())

        url_set = set()
        for link in BeautifulSoup(self.text, 'lxml').find_all("a"):
            href = link.get("href")

            try:
                url_set.add(URL.of(href, base_url))
            except Exception:
                continue

        return URLSet(url_set)
