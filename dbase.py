"""
sqlite3 interface for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

import sqlite3 as sqlite3
from config import ADMIN_ID, DEVELOPER_ID


class DB:
    db_filename = ''
    connection = None
    cursor = None

    def __init__(self, db_filename='db.db', create_sql_filename='create.sql'):
        """
        The __init__ function is called when the class is instantiated.
        It sets up the database connection and creates all tables if they don't exist.

        :param self: Represent the instance of the class
        :param db_filename: Specify the name of the database file
        :param create_sql_filename: Specify the name of the file with sql commands for creating tables
        :return: Nothing, but it creates the connection to the database
        """
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
        """
        The open_connection function opens a connection to the database and creates a cursor object.
        The cursor is used to execute SQL commands.

        :param self: Represent the instance of the class
        :return: The connection object
        """
        self.connection = sqlite3.connect(self.db_filename)
        self.cursor = self.connection.cursor()

    def add_user(self, tgid, chat_id):
        """
        The add_user function takes in a Telegram user ID and a chat ID,
        and adds the user to the database if they are not already present.
        It returns True if the user was added successfully, or False otherwise.

        :param self: Represent the instance of the class
        :param tgid: Store the telegram id of a user
        :param chat_id: Store the chat_id of the user in the database
        :return: True if the user was added to the database
        """
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
        """
        The get_all_users function returns a list of all users in the database.

        :param self: Represent the instance of the object itself
        :return: A list of tuples
        """
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
        """
        The delete_all_users function deletes all users from the database.

        :param self: Represent the instance of the class
        :return: Nothing
        """
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
    """
    The user_is_admin function checks if the user is an admin or developer.
        Args:
            args (list): A list of arguments passed to the function.

    :param *args: Pass a variable number of arguments to the function
    :return: True if the user is an admin, false otherwise
    """
    tgid = args[0].from_user.id
    return ADMIN_ID == tgid or DEVELOPER_ID == tgid


dbase = DB()
