import sqlite3 as sqlite
from contextlib import closing
import csv


def connect_db():
    return sqlite.connect('data.db')

def init_db():
    with closing(connect_db()) as db:
        db.cursor().execute("""drop table if exists filters;""")
        db.cursor().execute("""create table filters (
            name text,
            filter text
        );""")


    #     db.cursor().execute("""
    #     create table suggestions(
    #     id integer primary key autoincrement,
    #     name text,
    #     location text,
    #     phone text,
    #     email text,
    #     description text
    # );""")

        db.commit()
        print "commited"

init_db()

# with open('./data.csv', 'rb') as f:
#     with closing(connect_db()) as db:
#             db.text_factory = str
#             csvr = csv.reader(f)
#             row = []
#             for i in csvr:
#                 row = [x for x in i]
#                 row.insert(0,None)
#                 print row
#                 db.cursor().execute("insert into organizations values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row)
#             db.commit()

with open('./filters.csv', 'rb') as f:
    with closing(connect_db()) as db:
            db.text_factory = str
            csvr = csv.reader(f)
            row = []
            for i in csvr:
                row = [x for x in i]
                
                print row
                db.cursor().execute("insert into filters values(?,?)", row)
            db.commit()