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


async def switch():
    await asyncio.sleep(0)


async def get_2():
    print('5')
    await asyncio.sleep(0)
    print('6')
    await asyncio.sleep(0)
    print('7')
    await asyncio.sleep(0)
    print('8')


async def get_1():
    i = 10
    while i < 20:
        print(i)
        await asyncio.sleep(0)
        i += 1


async def main():
    task2 = asyncio.create_task(get_1())
    task = asyncio.create_task(get_2())
    await task2
    await task

    pass

asyncio.run(main())
