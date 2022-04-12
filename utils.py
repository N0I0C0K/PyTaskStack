from typing import *
from pydantic import BaseModel
import logging
from chardet import detect

logging.basicConfig(filename='./log/test.log',
                    level=logging.DEBUG, encoding='utf-8')


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
    token: str                        # 密钥
    session_id: str                   # session id
    session_name: str                 # 任务名称
    session_command: str              # 任务需要执行的命令
    stdout_log: Optional[str] = None  # 标准输出输出到哪个文件
    stderr_log: Optional[str] = None  # 标准错误输出到哪个文件


def autoDecode(s: bytes) -> str:
    '''
    获取`s`对应的解码, 自动判断`s`的编码方式
    '''
    if len(s) == 0:
        return ''
    encoding = detect(s)
    return s.decode(encoding['encoding'])


if __name__ == '__main__':
    # print(autoDecode('张席是是假的吧就舍不得节哀顺便打不'.encode('gbk')))
    pass
