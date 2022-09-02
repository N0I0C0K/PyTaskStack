# coding: utf-8
from sqlalchemy import Column, Float, Text, Boolean, Integer, Table
from sqlalchemy.ext.declarative import declarative_base
from Utils import format_time

__all__ = ['SessionInfo', 'TaskInfo']


Base = declarative_base()
metadata = Base.metadata


def format_output(s: str) -> str:
    return '- '+s.replace('\n', '\n- ')


class SessionInfo(Base):
    __tablename__ = 'SessionInfo'

    id = Column(Text, primary_key=True)
    invoke_time = Column(Float, nullable=False)
    finish_time = Column(Float, nullable=False)
    task_id = Column(Text, nullable=False)
    command = Column(Text, nullable=False)
    std_out = Column(Text, nullable=True)
    std_err = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f'''======== Session {self.id} ========
execute time   : {format_time(self.invoke_time)}-{format_time(self.finish_time)}
execute command: {self.command}
task id        : {self.task_id}
std_out:
{format_output(self.std_out)}
std_err:
{format_output(self.std_err)}
======== End ========
'''


class TaskInfo(Base):
    __tablename__ = 'TaskInfo'

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)
    create_time = Column(Float, nullable=False)
    command = Column(Text, nullable=False)
    crontab_exp = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f'Task {self.id} {self.name}=> create at:{format_time(self.create_time)}, "{self.command}", {self.crontab_exp}, {self.active}'


class UserInfo(Base):
    __tablename__ = 'User'

    username = Column(Text, primary_key=True)
    pwd = Column(Text, nullable=False)
    salt = Column(Text, nullable=False)
    create_time = Column(Float, nullable=False)
