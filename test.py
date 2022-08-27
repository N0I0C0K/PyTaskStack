import sqlite3
from Data import dataManager
from sqlalchemy import select
from Data.models import SessionInfo, TaskInfo


def print_all_session_info():
    with dataManager.get_session() as sess:
        stmt = select(SessionInfo)
        for ses in sess.scalars(stmt):
            print(ses)


def print_all_task_info():
    with dataManager.get_session() as sess:
        stmt = select(TaskInfo)
        for ses in sess.scalars(stmt):
            print(ses)


def get_all_session_info():
    with dataManager.get_session() as sess:
        res = sess.query(SessionInfo)
        print('\n'.join(map(str, res.all())))


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
get_all_session_info()
