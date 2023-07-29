# -----------------------------------------------------------
# sqlite3 interface for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# -----------------------------------------------------------

import sqlite3 as sqlite3
from config import ADMIN_ID, DEVELOPER_ID


class DB:
    db_filename = ''
    connection = None
    cursor = None

    def __init__(self, db_filename='db.db', create_sql_filename='create.sql'):
        self.db_filename = db_filename
        try:
            self.open_connection()
            # создание таблиц
            with open(create_sql_filename) as f:
                self.cursor.executescript(f.read())
            self.connection.commit()
        except sqlite3.Error as error:
            print("SQLite error", error)
        finally:
            if self.connection:
                self.connection.close()

    def open_connection(self):
        self.connection = sqlite3.connect(self.db_filename)
        self.cursor = self.connection.cursor()

    def add_user(self, tgid, chat_id):
        try:
            self.open_connection()
            self.cursor.execute(f"SELECT * FROM users WHERE tgid = {tgid}")
            records = self.cursor.fetchall()
            if len(records) == 0:
                self.cursor.execute(f"INSERT INTO users VALUES ('{tgid}','{chat_id}')")
                self.connection.commit()
                return True
            else:
                return False
        except sqlite3.Error as error:
            print("SQLite error:", error)
        finally:
            if self.connection:
                self.connection.close()

    def get_all_users(self):
        try:
            self.open_connection()
            self.cursor.execute(f"SELECT * FROM users")
            records = self.cursor.fetchall()
            return records
        except sqlite3.Error as error:
            print("SQLite error:", error)
        finally:
            if self.connection:
                self.connection.close()

    def delete_all_users(self):
        try:
            self.open_connection()
            self.cursor.execute("DELETE FROM users")
            self.connection.commit()
        except sqlite3.Error as error:
            print("SQLite error:", error)
        finally:
            if self.connection:
                self.connection.close()


async def user_is_admin(*args):
    tgid = args[0].from_user.id
    return ADMIN_ID == tgid or DEVELOPER_ID == tgid


dbase = DB()
