from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional, Any, List
from urllib.parse import urljoin


@dataclass(init=False, unsafe_hash=True, frozen=True)
class URL:
    ABSOLUTE_URL_REGEX = re.compile(r"^https?://[\w/:%#\$&\?\(\)~\.=\+\-]+")
    absolute: str

    def __init__(self, url: str):
        assert url, "URLは必須です。"
        assert isinstance(url, str), "URLに{}が指定されています。文字列を指定して下さい。".format(type(url))
        assert self.ABSOLUTE_URL_REGEX.match(url), "{}は完全URLではありません。完全URLを指定して下さい。".format(url)
        super().__setattr__("absolute", url)

    @staticmethod
    def of(url: str, from_url: URL) -> Optional[URL]:
        if URL.ABSOLUTE_URL_REGEX.match(url):
            return URL(url)
        return URL(urljoin(from_url.absolute, url))

    def match(self, regex: re.Pattern) -> bool:
        return regex.match(self.absolute) is not None

    def extract(self, regex: re.Pattern) -> Optional[URL]:
        optional_match: List[Any] = regex.findall(self.absolute)
        if optional_match is None:
            return None
        return URL(optional_match[0])
