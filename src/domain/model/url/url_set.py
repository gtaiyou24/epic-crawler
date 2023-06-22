from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Set

from domain.model.url import URL


@dataclass(init=False, unsafe_hash=True, frozen=True)
class URLSet:
    set: Set[URL]

    def __init__(self, set: Set[URL]):
        assert isinstance(set, Set), "URL一覧にはSet型を指定してください"
        super().__setattr__("set", set)

    def filter_by_regex(self, regex: re.Pattern) -> URLSet:
        return URLSet(set(url for url in self.set if url.match(regex)))
