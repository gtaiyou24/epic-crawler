from di import DIContainer, DI

from application.crawl.service import PaginationApplicationService, ScrollApplicationService, \
    RecursiveApplicationService
from domain.model.browser import Browser
from domain.model.page import PageService
from domain.model.url import URLRepository
from port.adapter.service.browser import ChromeBrowser
from port.adapter.service.page import AsyncPageService
from port.adapter.standalone.inmemory import InMemoryURLRepository


def crawl(algorithm: str, **kwargs):
    if algorithm == 'scroll':
        seed_url = kwargs.get("seed_url")
        detail_url_regex = kwargs.get("detail_url_regex")
        more_selector = kwargs.get("more_selector") if kwargs.get("more_selector") else None

        DIContainer.instance().register(DI.of(Browser, {}, ChromeBrowser))
        DIContainer.instance().register(DI.of(URLRepository, {}, InMemoryURLRepository))

        scroll_application_service = DIContainer.instance().resolve(ScrollApplicationService)
        scroll_application_service.crawl(seed_url, detail_url_regex, more_selector)
    elif algorithm == 'pagination':
        seed_url = kwargs.get("seed_url")
        regex_to_save = kwargs.get("regex_to_save")
        regex_to_crawl = kwargs.get("regex_to_crawl")

        pagination_application_service = DIContainer.instance().resolve(PaginationApplicationService)

        DIContainer.instance().register(DI.of(PageService, {}, AsyncPageService))
        DIContainer.instance().register(DI.of(URLRepository, {}, InMemoryURLRepository))

        pagination_application_service.crawl(seed_url, regex_to_crawl, regex_to_save)
    elif algorithm == 'recursive':
        seed_url = kwargs.get("seed_url")
        regex_to_save = kwargs.get("regex_to_save")
        regex_to_crawl = kwargs.get("more_selector")

        DIContainer.instance().register(DI.of(Browser, {}, ChromeBrowser))
        DIContainer.instance().register(DI.of(URLRepository, {}, InMemoryURLRepository))

        recursive_application_service = DIContainer.instance().resolve(RecursiveApplicationService)
        recursive_application_service.crawl(seed_url, regex_to_save, regex_to_crawl)
