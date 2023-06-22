import atexit
import csv

from slf4py import set_logger

from domain.model.url import URLRepository, URL


@set_logger
class InMemoryURLRepository(URLRepository):
    __urls = set()

    def __init__(self):
        atexit.register(self.__to_csv)

    def save(self, url: URL):
        self.__urls.add(url)
        self.log.debug("URL : {}件".format(len(self.__urls)))

    def __to_csv(self):
        with open('url.csv', 'w') as f:
            write = csv.writer(f)
            write.writerow(['', 'url'])
            write.writerows([[i, url.absolute] for i, url in enumerate(self.__urls)])
