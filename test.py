import sqlite3
from Data import dataManager
from sqlalchemy import select
from Data.models import SessionInfo, TaskInfo
import asyncio


def print_all_session_info():
    with dataManager.get_session() as sess:
        stmt = select(SessionInfo)
        for ses in sess.scalars(stmt):
            print(ses)


async def print_all_task_info():
    print('1')
    with dataManager.get_session() as sess:
        stmt = select(TaskInfo)
        for ses in sess.scalars(stmt):
            print(ses)
    await asyncio.sleep(2)
    print('2')


async def get_all_session_info():
    print('3')
    with dataManager.get_session() as sess:
        res = sess.query(SessionInfo)
        print('\n'.join(map(str, res.all())))
    await asyncio.sleep(2)
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


async def main():
    print(
        asyncio.coroutines.iscoroutinefunction(print_all_task_info))
    task = asyncio.create_task(print_all_task_info())
    task2 = asyncio.create_task(get_all_session_info())
    await task
    await task2

    pass

asyncio.run(main())
