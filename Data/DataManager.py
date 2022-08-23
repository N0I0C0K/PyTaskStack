import sqlite3
from threading import Lock


class DataManager:
    def __init__(self) -> None:
        '''
        数据管理, 采用sqllit进行数据储存
        '''
        self.__conn = sqlite3.connect('data.db')
        self.conn_lock = Lock()


dataManager = DataManager()