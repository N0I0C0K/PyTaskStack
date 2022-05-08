import logging
import sys
from typing import *
from pydantic import BaseModel
from chardet import detect
#from ExecuteUnit import ExecuteUnit

__all__ = ['logger', 'SessionInfo', 'SessionForm',
           'FormRaw', 'autoDecode', 'set_color']

logging.basicConfig(filename='./log/test.log',
                    level=logging.INFO, encoding='utf-8')
logger = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class SessionInfo:
    token: str = None
    key: str = None
    stdout_log: str = None
    stderr_log: str = None
    session_id: str = None
    session_name: str = None
    session_command: str = None
    session_task: 'ExecuteUnit' = None

    def __init__(self) -> None:
        '''
        Session info的一个单元
        '''
        pass

    def __str__(self) -> str:
        return f'{self.session_id}:{self.session_name} => {self.session_command}'


class SessionForm(BaseModel):
    # key: str                        # 密钥
    session_id: str                   # session id
    session_name: str                 # 任务名称
    session_command: str              # 任务需要执行的命令
    stdout_log: Optional[str] = None  # 标准输出输出到哪个文件
    stderr_log: Optional[str] = None  # 标准错误输出到哪个文件


class FormRaw(BaseModel):
    data: str
    sign: str
    key: str
    nonce: str


def autoDecode(s: bytes) -> str:
    '''
    获取`s`对应的解码, 自动判断`s`的编码方式
    '''
    if len(s) == 0:
        return ''
    encoding = detect(s)
    return s.decode(encoding['encoding'])


color_support = True


class COLOR:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    DEFAULT = '\033[39m'


if sys.platform == "win32":
    try:
        # https://stackoverflow.com/questions/36760127/...
        # how-to-use-the-new-support-for-ansi-escape-sequences-in-the-windows-10-console
        from ctypes import windll
        kernel32 = windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:  # pragma: no cover
        color_support = False


def set_color(s: str, color: COLOR) -> str:
    if color_support:
        return f"{color}{s}{COLOR.DEFAULT}"
    return s


if __name__ == '__main__':
    # print(autoDecode('张席是是假的吧就舍不得节哀顺便打不'.encode('gbk')))
    pass
