from sqlalchemy import create_engine
from .models import Base


class DataManager:
    def __init__(self) -> None:
        '''
        数据管理, 采用sqllit进行数据储存
        '''
        self.engine = create_engine(
            'sqlite:///data.db', echo=True, future=True)

    def create_all_table(self):
        Base.metadata.create_all(self.engine)


dataManager = DataManager()
'''
数据管理单例
负责数据的存储
'''
