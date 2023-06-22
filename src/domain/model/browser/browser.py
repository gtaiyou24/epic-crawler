import abc

from domain.model.page import Page
from domain.model.url import URL


class Browser(abc.ABC):
    @abc.abstractmethod
    def browse(self, url: URL):
        pass

    @abc.abstractmethod
    def scroll(self):
        pass

    @abc.abstractmethod
    def exist(self, selector: str) -> bool:
        pass

    @abc.abstractmethod
    def click(self, selector: str):
        pass

    @abc.abstractmethod
    def download_page(self) -> Page:
        pass
