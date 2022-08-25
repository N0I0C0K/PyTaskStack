from pydantic import BaseModel
from typing import Optional


class TokenBase(BaseModel):
    token: str


class TaskForm(TokenBase):
    command: str
    name: Optional[str]
    crontab_exp: Optional[str]
