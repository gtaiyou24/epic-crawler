import abc

from domain.model.url import URL


class URLRepository(abc.ABC):
    @abc.abstractmethod
    def save(self, url: URL):
        pass
