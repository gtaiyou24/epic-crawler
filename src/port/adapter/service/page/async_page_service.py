import requests
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from domain.model.page import PageService, Page, HttpStatus
from domain.model.page.html import CharacterCode, HTML
from domain.model.url import URL


class AsyncPageService(PageService):
    CHROME_DRIVER_PATH = "/usr/bin/chromedriver"

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # ヘッドレスモード
        options.add_argument("--disable-gpu")  # 暫定的に必要なフラグ
        options.add_argument('--lang=ja-JP')  # 日本語対応
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-extensions")  # すべての拡張機能を無効にする
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-setuid-sandbox")
        options.add_argument("--start-maximized")  # 最小画面で起動
        # 速度改善のために、スマートフォンのユーザーエージェントを設定
        options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) " + \
                             "AppleWebKit/605.1.15 (KHTML, like Gecko) " + \
                             "Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone9,1;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1" + \
                             ";FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]")
        options.add_experimental_option('useAutomationExtension', False)  # Chrome拡張の利用をOFF
        self.__web_driver = webdriver.Chrome(executable_path=self.CHROME_DRIVER_PATH, options=options)
        super().__init__()

    def _download(self, url: URL, connect_timeout: float, read_timeout: float) -> Page:
        self.__web_driver.get(url.absolute)
        # 最下部までスクロールする
        self.__web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # ページの読み込みが完了するまで待機する
        wait = WebDriverWait(self.__web_driver, read_timeout)
        wait.until(expected_conditions.presence_of_all_elements_located)

        page_url = URL(self.__web_driver.current_url)
        response = requests.get(self.__web_driver.current_url, timeout=(connect_timeout, read_timeout))
        http_status = HttpStatus.value_of(response.status_code)
        html = HTML(self.__web_driver.page_source, CharacterCode.value_of(response.apparent_encoding))
        return Page(page_url, http_status, html)
