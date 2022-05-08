import rsa
import Crypto.Cipher.AES as CryCes
import base64
import os
import secrets
import json
from CryptoCore import cryptoCore
from typing import *
from utils import *
from collections import defaultdict
from ExecuteUnit import ExecuteUnit


class SessionCore:

    def __init__(self):
        '''
        会话核心组件, 包括`session`的存储, 验证, 获取
        :param private_key: private key, 默认为`None`会读取AuthCore文件的目录下的`private_key`文件
        '''
        self.sessionDict: Dict[str, SessionInfo] = defaultdict(
            SessionInfo)  # 储存session信息
        '''
        里面储存着所有session的授权信息
        `session_id`=>`{'session_id':'id','key':'key','token':'token'}`
        '''

    def newSession(self) -> Tuple[str, str]:
        '''
        获得一个新的`session`, 并且挂起.
        '''
        sessid = secrets.token_urlsafe(32)
        self.addSession(sessid)
        return sessid

    def addSession(self, session_id) -> bool:
        '''
        将一个session信息挂起
        '''
        if session_id in self.sessionDict:
            return False
        self.sessionDict[session_id].__dict__.update(
            {'session_id': session_id})
        return True

    def updateSessionFromSessionForm(self, session_id: str, data: SessionForm):
        assert session_id in self.sessionDict
        session = self.sessionDict[session_id]
        session.__dict__.update(data.dict())
        logger.info('%s', str(session))

    def updateSessionInfoByRaw(self, form: FormRaw) -> str:
        decodeForm = cryptoCore.DecodeFormRaw(form)
        self.updateSessionFromSessionForm(decodeForm.session_id, decodeForm)
        return decodeForm.session_id

    def runSession(self, session_id: str):
        assert session_id in self.sessionDict
        execUnit = ExecuteUnit(self.sessionDict[session_id])
        self.sessionDict[session_id].session_task = execUnit

    def sessionFinished(self, session_id: str) -> bool:
        '''
        判断`session_id`是否运行完毕
        '''
        assert session_id in self.sessionDict
        session = self.sessionDict[session_id]
        assert session.session_task is not None
        return session.session_task.finished()

    def getSessionInfo(self, session_id: str) -> Union[SessionInfo, None]:
        if session_id not in self.sessionDict:
            return None
        return self.sessionDict[session_id]

    def getSessionOutPut(self, session_id: str) -> Tuple[str, str]:
        '''
        获得`session_id`的输出, 如果还在 '运行' 则返回`('','')`, 如果不存在则抛出错误
        :return :Tuple[stdout, stderr]
        '''
        assert session_id in self.sessionDict, '非法session'
        session = self.sessionDict[session_id]
        if session.session_task is None:
            return '', ''
        task: ExecuteUnit = session.session_task
        if not task.finished():
            return ('', 'ERROR:task is running')
        return (task.stdout, task.stderr)


if __name__ == '__main__':
    # generateRsa()
    pass

sessionManager = SessionCore()
'''
认证组件单例,会话核心组件, 包括`session`的存储, 获取
'''
