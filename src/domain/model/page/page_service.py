import abc
import time

from retrying import retry

from domain.model.page import Page
from domain.model.url import URL


class PageService(abc.ABC):

    def __init__(self, interval=3.0, connect_timeout=6.0, read_timeout=10.0):
        """
        :param interval: リクエスト間隔を秒数で指定します。
        :param connect_timeout: 相手のサーバーと接続を確立する(establish a connection)までの待機時間(秒)を指定します。
        TCPの仕様では、3秒(以下?)ごとに再送信(retransmit)するらしいので、3の倍数が良いようです。
        相手のサーバーがダウンしてる場合は、接続を確立できないはずなので、このconnect timeoutに引っかかります。
        :param read_timeout: サーバーがレスポンスを返してくるまでの待機時間(秒)を指定します。
        接続確立後の待機時間ですので、相手のサーバーダウンというよりは、相手が応答を返すのに時間がかかっているということになります。
        """
        self.__interval = interval
        self.__connect_timeout = connect_timeout
        self.__read_timeout = read_timeout

    # リトライ設定
    # - stop_max_attempt_number : 最大リトライ回数
    # - wait_exponential_multiplier : 指数関数的なwaitをとる場合は、初回のwaitをミリ秒単位で指定する
    @retry(stop_max_attempt_number=3, wait_exponential_multiplier=1000)
    def download(self, url: URL) -> Page:
        """
        URL指定でPageを取得する

        ビジネスルール
         1. 間隔を設ける: 少なくとも1秒は間隔を空けるようにする。
         2. タイムアウトを設定する: サイトの応答が著しく悪い場合があります。そのような場合は、タイムアウトを設定しましょう。
         3. リトライをする: 普段のサイトの応答が悪くなくとも、タイミングによってはエラーが返されることがあります。なるべくクロール時に同時性を持ったデータを収集したい場合は、リトライする仕組みを入れると良いでしょう。

        :param url:
        :return Page:
        """
        # 間隔を空ける
        time.sleep(self.__interval)

        # タイムアウトを設定
        return self._download(url, self.__connect_timeout, self.__read_timeout)

    @abc.abstractmethod
    def _download(self, url: URL, connect_timeout: float, read_timeout: float) -> Page:
        pass
