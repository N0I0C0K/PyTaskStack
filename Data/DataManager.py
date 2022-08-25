from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.engine import ScalarResult
from .models import Base


class DataManager:
    def __init__(self) -> None:
        '''
        数据管理, 采用sqllit进行数据储存
        '''
        self.engine = create_engine(
            'sqlite:///data.db', echo=True, future=True)
        self.create_all_table()

    def get_session(self) -> Session:
        return Session(self.engine)

    def create_all_table(self):
        Base.metadata.create_all(self.engine)

    def has_item_by_id(self, tarType: Base, tar_id: str) -> bool:
        with self.get_session() as sess:
            stmt = select(tarType).where(tarType.id == tar_id)
            res: ScalarResult = sess.scalars(stmt)
            try:
                res.one()
            except:
                return False
            else:
                return True


dataManager = DataManager()
'''
数据管理单例
负责数据的存储
'''
