from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.engine import ScalarResult
from sqlalchemy.log import rootlogger
import logging
from .models import Base


class DataManager:
    def __init__(self) -> None:
        '''
        数据管理, 采用sqllit进行数据储存
        '''
        self.engine = create_engine(
            'sqlite:///data.db', echo=False, future=True)
        rootlogger.setLevel(logging.ERROR)
        self.create_all_table()

    def get_session(self) -> Session:
        return Session(self.engine)

    @property
    def session(self) -> Session:
        return self.get_session()

    def create_all_table(self):
        Base.metadata.create_all(self.engine)

    def has_item_by_id(self, tarType: Base, tar_id: str) -> bool:
        with self.get_session() as sess:
            res = sess.query(tarType).filter(tarType.id == tar_id)
            return res.first() is not None


dataManager = DataManager()
'''
数据管理单例
负责数据的存储
'''
