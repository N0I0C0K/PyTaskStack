import sqlite3
from Data import dataManager
from sqlalchemy import select
from Data.models import SessionInfo, TaskInfo
import asyncio
import time


def print_all_session_info():
    print('5')
    with dataManager.get_session() as sess:
        stmt = select(SessionInfo)
        for ses in sess.scalars(stmt):
            print(ses)
    print('6')


def print_all_task_info():
    print('1')
    with dataManager.get_session() as sess:
        stmt = select(TaskInfo)
        for ses in sess.scalars(stmt):
            print(ses)
    print('2')


def get_all_session_info():
    print('3')
    with dataManager.get_session() as sess:
        res = sess.query(SessionInfo)
        print('\n'.join(map(str, res.all())))
    print('4')


def del_table(name):
    conn = sqlite3.connect('./data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f'drop table {name}')
    conn.commit()


print('test')

# del_table('SessionInfo')
# print_all_session_info()
# print_all_task_info()
# get_all_session_info()


# async def get_2():
#     print('5')
#     await asyncio.sleep(1)
#     with dataManager.get_session() as sess:
#         stmt = select(SessionInfo)
#         for ses in sess.scalars(stmt):
#             print(ses)
#     print('6')


# async def get_1():
#     print('1')
#     await asyncio.sleep(1)
#     with dataManager.get_session() as sess:
#         stmt = select(TaskInfo)
#         for ses in sess.scalars(stmt):
#             print(ses)
#     print('2')


# async def main():
#     task2 = asyncio.create_task(get_1())
#     task = asyncio.create_task(get_2())
#     await task2
#     await task

#     pass

# asyncio.run(main())

class TestA:
    def a(self):
        print('a')
        del self

    def __del__(self):
        print('del')


a = TestA()
a.a()
print(a)
a = '123'
print(a)
print('end')
