from __future__ import annotations

from enum import Enum


class HttpStatus(Enum):
    UNKNOWN = 0
    OK = 200

    # 3xx

    # 4xx
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    REQUEST_TIMEOUT = 408

    # 5xx
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504

    @staticmethod
    def value_of(status: int) -> HttpStatus:
        if status == HttpStatus.OK.value:
            return HttpStatus.OK
        if status == HttpStatus.BAD_REQUEST.value:
            return HttpStatus.BAD_REQUEST
        if status == HttpStatus.UNAUTHORIZED.value:
            return HttpStatus.UNAUTHORIZED
        if status == HttpStatus.FORBIDDEN.value:
            return HttpStatus.FORBIDDEN
        if status == HttpStatus.NOT_FOUND.value:
            return HttpStatus.NOT_FOUND
        if status == HttpStatus.METHOD_NOT_ALLOWED.value:
            return HttpStatus.METHOD_NOT_ALLOWED

        if status == HttpStatus.INTERNAL_SERVER_ERROR.value:
            return HttpStatus.INTERNAL_SERVER_ERROR

        return HttpStatus.UNKNOWN

    def is_200(self) -> bool:
        return self == HttpStatus.OK
