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

from Api.utils import *
print(make_response(CodeResponse.INVALID_TOKEN))
