# import sqlite3
# import sqlalchemy

# from Data import dataManager

# conn = sqlite3.connect('./data.db')
# conn.row_factory = sqlite3.Row
# cur = conn.cursor()

# cur.execute('drop table Session')
# conn.commit()

# cur.execute('''create table Session(
#     id text primary key not null,
#     invoke_time float not null
# )''')
# conn.commit()


# # cur.execute('select * from sqlite_master')
# # a: sqlite3.Row = None
# # for a in cur.fetchall():
# #     print(a.keys())
# #     print(tuple(a))
# '''
# create table Session(
#     id text primary key not null,
#     invoke_time float not null
# )


# '''

# dataManager.create_all_table()

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


def del_table(name):
    conn = sqlite3.connect('./data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(f'drop table {name}')
    conn.commit()


# del_table('TaskInfo')
print_all_session_info()
# print_all_task_info()
raise ValueError('aaa')
