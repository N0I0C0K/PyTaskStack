# coding: utf-8
from sqlalchemy import Column, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
import time

__all__ = ['SessionInfo', 'TaskInfo']


def format_time(t: float) -> str:
    return time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime(t))


Base = declarative_base()
metadata = Base.metadata


class SessionInfo(Base):
    __tablename__ = 'SessionInfo'

    id = Column(Text, primary_key=True)
    invoke_time = Column(Float, nullable=False)
    task_id = Column(Text, nullable=False)
    command = Column(Text, nullable=False)
    std_out = Column(Text, nullable=True)
    std_err = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f'Session, {format_time(self.invoke_time)}, {id}=> command:{self.command} ,std_out:{self.std_out}, std_err:{self.std_err}'


class TaskInfo(Base):
    __tablename__ = 'TaskInfo'

    id = Column(Text, primary_key=True)
    name = Column(Text, nullable=False)
    active = Column(Boolean, nullable=False)
    create_time = Column(Float, nullable=False)
    command = Column(Text, nullable=False)
    crontab_exp = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f'Task {self.id} {self.name}=> create at:{format_time(self.create_time)}, {self.command}, {self.crontab_exp}, {self.active}'
