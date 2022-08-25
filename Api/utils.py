from typing import Optional
from enum import Enum

__all__ = ['CodeResponse', 'make_response']


class CodeResponse(Enum):
    SUCCESS = 200, 'success'
    INVALID_TOKEN = 301, 'invalid token'
    UNKONOW_ERR = 500, 'unknow error'


def make_response(code: CodeResponse, data: Optional[dict] = None) -> dict:
    cod, msg = code.value
    return {'code': cod, 'msg': msg, 'data': data}
