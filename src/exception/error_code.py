from __future__ import annotations

from enum import Enum

from logger import logger


@logger
class ErrorLevel(Enum):
    WARN = 'WARN'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

    def to_logger(self, error_code: ErrorCode, detail: str):
        msg = "[Code] {code} [Message] {message} [Detail] {detail}".format(
            code=error_code.name, message=error_code.message, detail=detail)

        if self == ErrorLevel.WARN:
            self.log.warn(msg)
        elif self == ErrorLevel.ERROR:
            self.log.error(msg)
        elif self == ErrorLevel.CRITICAL:
            self.log.critical(msg)
        else:
            self.log.info(msg)


class ErrorCode(Enum):
    COMMON_1001 = ('内部エラーが発生しました。', ErrorLevel.CRITICAL)
    DB_CAN_NOT_CONNECT_TO_DATABASE = ('データベースへの接続に失敗しました。', ErrorLevel.CRITICAL)
    DB_CLIENT_ERROR = ('クライアントエラーが発生しました。', ErrorLevel.ERROR)
    DB_NOT_FOUND = ('該当データが見つかりません。', ErrorLevel.ERROR)
    DB_TIME_OUT = ('タイムアウトが発生しました。', ErrorLevel.WARN)
    ITEM_IS_NOT_FOUND = ("該当アイテムが見つかりませんでした。", ErrorLevel.WARN)
    BRAND_IS_NOT_FOUND = ("該当ブランドが見つかりませんでした。", ErrorLevel.WARN)

    def __init__(self, message: str, error_level: ErrorLevel):
        self.message = message
        self.error_level = error_level

    def log(self, detail: str):
        self.error_level.to_logger(self, detail)
