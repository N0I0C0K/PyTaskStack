import rsa
import base64
import os
import secrets
from typing import *
from utils import *
from collections import defaultdict
from ExecuteUnit import ExecuteUnit


class SessionCore:
    sessionDict: Dict[str, SessionInfo] = None
    '''
    里面储存着所有session的授权信息
    `session_id`=>`{'session_id':'id','key':'key','token':'token'}`
    '''

    def __init__(self, private_key: str = None) -> None:
        '''
        会话核心组件, 包括`session`的存储, 验证, 获取
        :param private_key: private key, 默认为`None`会读取AuthCore文件的目录下的`private_key`文件
        '''
        self.sessionDict = defaultdict(SessionInfo)  # 储存session信息
        if private_key is None:
            key_path = os.path.dirname(__file__)+'\\private_key'
            if not os.path.exists(key_path):
                raise ValueError(f'{key_path} 不存在, 未能初始化验证组件')
            with open(key_path, 'r', encoding='utf-8') as file:
                private_key = file.read()
        self.__privateKey = rsa.PrivateKey.load_pkcs1(
            private_key.encode('utf-8'))

    def newSession(self) -> Tuple[str, str]:
        '''
        获得一个新的`session`, 并且挂起.
        '''
        sessid, key = secrets.token_urlsafe(32), secrets.token_hex(16)
        self.addSession(sessid, key)
        return (sessid, key)

    def addSession(self, session_id, key: str) -> bool:
        '''
        将一个session信息挂起
        '''
        if session_id in self.sessionDict:
            return False
        self.sessionDict[session_id].__dict__.update(
            {'session_id': session_id, 'key': key})
        return True

    def verify(self, session_id, token: str) -> bool:
        '''
        验证`token`的正确性
        '''
        if session_id not in self.sessionDict:
            return False
        _token = base64.b64decode(token)
        session_info: SessionInfo = self.sessionDict[session_id]
        if session_info.token is None:
            if rsa.decrypt(_token, self.__privateKey).decode() == session_info.key:
                return True
            else:
                return False
        else:
            return session_info.token == token

    def updateSessionInfoByDict(self, session_id: str, data: dict):
        if session_id not in self.sessionDict:
            raise KeyError(f'{session_id} not in sessionDict')
        self.sessionDict[session_id].__dict__.update(data)

    def runSession(self, session_id: str):
        if session_id not in self.sessionDict:
            raise KeyError(f'{session_id} not in session dict')
        execUnit = ExecuteUnit(self.sessionDict[session_id])
        self.sessionDict[session_id].session_task = execUnit


def generateRsa():
    pub, pri = rsa.newkeys(1024)
    with open('./private_key', 'wb') as file:
        file.write(pri.save_pkcs1())
    with open('./public_key', 'wb') as file:
        file.write(pub.save_pkcs1())


if __name__ == '__main__':
    # generateRsa()
    pass

sessionManager = SessionCore()
'''
认证组件单例,会话核心组件, 包括`session`的存储, 验证, 获取
'''
