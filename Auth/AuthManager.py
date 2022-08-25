class AuthManager:
    def __init__(self) -> None:
        '''
        鉴权中心, 负责用户得安全访问. token的存储
        '''
        pass

    def get_token(self, username: str, pwd: str) -> str:
        # TODO get token
        return '123'

    def verify_token(self, token: str) -> str:
        # TODO verify_token
        return True


auth_manager = AuthManager()
