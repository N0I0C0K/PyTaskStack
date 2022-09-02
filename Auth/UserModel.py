import time

TOKEN_DURATION = 3600*24*7  # 7天


class UserModel:
    id: str
    username: str
    pwd: str  # 加密后
    salt: str


class TokenModel:
    token: str
    username: str
    generate_time: float
    duration: float

    def __init__(self, username: str, token: str, *, duration: float = 0) -> None:
        self.username = username
        self.token = token
        self.generate_time = time.time()
        self.duration = duration if duration > 0 else TOKEN_DURATION
