from pydantic import BaseModel
from typing import Optional

# TODO 数据加密传输


class TokenBase(BaseModel):
    token: str


class TaskForm(TokenBase):
    command: str
    name: Optional[str]
    crontab_exp: Optional[str]
