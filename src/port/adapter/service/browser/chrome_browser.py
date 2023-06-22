import requests
from retrying import retry
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from slf4py import set_logger
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from domain.model.browser import Browser
from domain.model.page import Page, HttpStatus
from domain.model.page.html import HTML, CharacterCode
from domain.model.url import URL


@set_logger
class ChromeBrowser(Browser):
    USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone9,1;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]'

    def __init__(self, wait: int = 10):
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
        options.add_argument(f'--user-agent={self.USER_AGENT}')
        options.add_experimental_option('useAutomationExtension', False)  # Chrome拡張の利用をOFF
        self.__web_driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
            options=options
        )
        # self.__web_driver = webdriver.Chrome(executable_path=self.__CHROME_DRIVER_PATH, options=options)
        self.__wait = wait

    def browse(self, url: URL):
        self.__web_driver.get(url.absolute)
        self.scroll()

    @retry(stop_max_attempt_number=3, wait_exponential_multiplier=3000)
    def scroll(self):
        # 最下部までスクロールする
        self.__web_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # ページの読み込みが完了するまで待機する
        wait = WebDriverWait(self.__web_driver, self.__wait)
        wait.until(expected_conditions.presence_of_all_elements_located)

    def exist(self, selector: str) -> bool:
        try:
            return self.__web_driver.find_element(by=By.CSS_SELECTOR, value=selector) is not None
        except NoSuchElementException:
            return False

    def click(self, selector: str):
        self.__web_driver.execute_script(
            "arguments[0].click();", self.__web_driver.find_element(by=By.CSS_SELECTOR, value=selector))

    def download_page(self) -> Page:
        page_url = URL(self.__web_driver.current_url)
        response = requests.get(
            self.__web_driver.current_url,
            headers={'User-Agent': self.USER_AGENT},
            timeout=(12.0, 6.0)
        )
        http_status = HttpStatus.value_of(response.status_code)
        html = HTML(self.__web_driver.page_source, CharacterCode.value_of(response.apparent_encoding))
        return Page(page_url, http_status, html)
