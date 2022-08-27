from typing import Optional, Callable, Any, TypeVar
from collections import Iterable
import asyncio
from collections.abc import Coroutine
from enum import Enum
from .models import TokenBase
from Auth import auth_manager
from functools import wraps

__all__ = ['CodeResponse', 'make_response', 'require_token', 'catch_error']


class CodeResponse(Enum):
    SUCCESS = 200, 'success'
    INVALID_TOKEN = 301, 'invalid token'
    UNKONOW_ERR = 500, 'unknow error'


def make_response(code: CodeResponse, data: Optional[dict] = None) -> dict:
    cod, msg = code.value
    return {'code': cod, 'msg': msg, 'data': data}


T = TypeVar('T')


def find_type_arg(type: T, *args) -> T:
    for it in args:
        if not isinstance(it, Iterable):
            continue
        for t in it:
            if isinstance(t, type):
                return t
    return None


def catch_error(func: Callable) -> Callable:
    '''
    捕捉正常程序未捕获到的错误, 并且返回错误.
    '''
    @wraps(func)
    def dec(*args, **kwargs):
        re = None
        try:
            re = func(*args, **kwargs)
        except Exception as err:
            return make_response(CodeResponse.UNKONOW_ERR, {'err_msg': str(err)})
        else:
            return re

    @wraps(func)
    async def async_dec(*args, **kwargs):
        re = None
        try:
            re = await func(*args, **kwargs)
        except Exception as err:
            return make_response(CodeResponse.UNKONOW_ERR, {'err_msg': str(err)})
        else:
            return re
    return async_dec if asyncio.coroutines.iscoroutinefunction(func) else dec


def require_token(func: Callable[[TokenBase, ], Any]) -> Callable[[TokenBase, ], Any]:
    '''
    token验证
    '''
    @wraps(func)
    def dec(*args, **kwargs):
        token_form = find_type_arg(TokenBase, args, kwargs.values())
        if not token_form or not auth_manager.verify_token(token_form.token):
            return make_response(CodeResponse.INVALID_TOKEN)
        else:
            re = func(*args, **kwargs)
            return re

    @wraps(func)
    async def async_dec(*args, **kwargs):
        token_form = find_type_arg(TokenBase, args, kwargs.values())
        if not token_form or not auth_manager.verify_token(token_form.token):
            return make_response(CodeResponse.INVALID_TOKEN)
        else:
            re = await func(*args, **kwargs)
            return re
    return async_dec if asyncio.coroutines.iscoroutinefunction(func) else dec
