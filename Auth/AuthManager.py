import typing
import secrets
import asyncio
import time

from Crypto.Hash import MD5
from Data import dataManager
from Data.models import UserInfo
from re import match

from .UserModel import TokenModel

TokenStr = typing.NewType('TokenStr', str)


class AuthManager:
    def __init__(self) -> None:
        '''
        鉴权中心, 负责用户得安全访问. token的存储. 用户数据访问
        '''
        self.endfix_dict: typing.Dict[str, str] = dict()
        self.token_dict: typing.Dict[TokenStr, TokenModel] = dict()
        self.check_token_process: asyncio.Task = None

    def register(self, username: str, pwd: str) -> bool:
        failed_err = ValueError('未知错误')
        if username not in self.endfix_dict:
            raise failed_err
        salt = self.endfix_dict[username]
        with dataManager.session as sess:
            query = sess.query(UserInfo).filter(UserInfo.username == username)
            if query.first() is not None:
                raise failed_err
            user = UserInfo(username=username,
                            pwd=pwd,
                            salt=salt,
                            create_time=time.time())
            sess.add(user)
            sess.commit()
        return True

    def get_user_salt(self, username: str) -> str:
        with dataManager.session as sess:
            query = sess.query(UserInfo).filter(UserInfo.username == username)
            user: UserInfo = query.first()
            if user is None:
                raise ValueError('非法操作')
            return user.salt

    def open_session(self, username: str) -> str:
        if username in self.endfix_dict:
            return self.endfix_dict[username]
        if match(r'^[a-zA-Z0-9]{4,15}$', username) is None:
            raise ValueError('名称非法')
        endfix = secrets.token_hex(8)
        self.endfix_dict[username] = endfix
        return endfix

    def login(self, username: str, pwd: str) -> str:
        failed_err = ValueError('未能找到此用户或者密码错误')
        if username not in self.endfix_dict:
            raise failed_err
        endfix = self.endfix_dict[username]
        with dataManager.session as sess:
            query = sess.query(UserInfo).filter(UserInfo.username == username)
            user: UserInfo = query.first()
            if not user:
                raise failed_err
            original_pwd_encode = MD5.new(
                str(user.pwd+endfix).encode()).hexdigest()
            if pwd != original_pwd_encode:
                raise failed_err
            self.endfix_dict.pop(username)
            return self.__generate_token(username)

    def __generate_token(self, username: str) -> str:
        token_str = secrets.token_hex(16)
        token = TokenModel(username, token_str)
        self.token_dict[token_str] = token
        return token_str

    def verify_token(self, token: str) -> bool:
        if len(token) < 3:
            return False
        return token in self.token_dict

    def start_check_token_process(self, loop: asyncio.AbstractEventLoop):
        self.check_token_process = loop.create_task(self.check_token())

    async def check_token(self):
        while True:
            time_now = time.time()
            token_list = tuple(self.token_dict.keys())
            for token_str in token_list:
                token = self.token_dict[token_str]
                if token.generate_time+token.duration < time_now:
                    self.token_dict.pop(token_str)
            await asyncio.sleep(1)


auth_manager = AuthManager()
