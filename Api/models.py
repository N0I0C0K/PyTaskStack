from pydantic import BaseModel
from typing import Optional, List

# TODO 数据加密传输


class TokenBase(BaseModel):
    token: str


class TaskUploadForm(TokenBase):
    command: str
    name: Optional[str]
    crontab_exp: Optional[str]


class TaskQueryForm(TokenBase):
    task_id: List[str]
    require_active: Optional[bool] = False


class TaskDelForm(TokenBase):
    task_id: List[str]


class SessionQueryForm(TokenBase):
    session_id: List[str]


class SessionQueryByTaskForm(TokenBase):
    task_id: List[str]


class SessionDelForm(TokenBase):
    session_id: List[str]


class UserForm(BaseModel):
    username: str
    pwd: str
