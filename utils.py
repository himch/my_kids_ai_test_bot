"""
utils for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

import asyncio
from aiogram import types

from config import DEVELOPER_ID, ADMIN_ID
from dbase import dbase
from misc import bot


async def get_user_data(data, message):
    """
    The get_user_data function is used to get the user's Telegram ID and full name.
    It also adds the user to a database if they are not already in it.

    :param data: Store the data that is passed to this function
    :param message: Get the message from the user
    :return: A tuple with the user's data
    """
    data['db_tgid'] = message.from_user.id
    data['db_full_name'] = message.from_user.full_name
    return dbase.add_user(data['db_tgid'], message.chat.id)


async def print_user(tg_id, print_tg_id=True):
    """
    The print_user function takes a Telegram user ID and returns a string containing the
    user's name, with an HTML link to their profile. If the user is not in your contacts,
    the function will return &quot;-- утрачен --&quot; instead of their name.

    :param tg_id: Get the user's name and id
    :param print_tg_id: Indicate whether the user's telegram id should be displayed in the output
    :return: A string with a link to the user
    """
    try:
        user = await bot.get_chat(tg_id)
    except Exception:
        result = f'<a href="tg://user?id={tg_id}">-- утрачен --, id = {tg_id}</a>'
    else:
        last_name = '' if user.last_name is None else ' ' + str(user.last_name)
        full_name = user.first_name + last_name
        result = f'<a href="tg://user?id={tg_id}">{full_name}'
    return result + (f', id = {tg_id}</a>' if print_tg_id else '</a>')


async def print_user_list(message, users, row_index):
    """
    The print_user_list function is used to generate and print a clickable Telegram user list.
    It takes three arguments: message, users, row_index.
    The message argument is the Telegram bot's response to the user's request for a list of users.
    The users argument is an array of tuples containing information about each user in the database (e.g., id, username).
    The row_index argument specifies which element from each tuple should be printed as part of the list.

    :param message: Send the message to the user
    :param users: Pass the list of users to print
    :param row_index: Determine which column of the database to print
    :return: A list of users
    """
    if users and len(users) > 0:
        for row in users:
            await message.answer(await print_user(row[row_index]),
                                 reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Нет таких, список пуст",
                             reply_markup=types.ReplyKeyboardRemove())


async def send_info_to_dev_admin(st, keyboard=None):
    """
    The send_info_to_dev_admin function sends a message to the developer and admin.
        The function takes two arguments: st, which is the string that will be sent, and keyboard,
        which is an optional argument for a custom keyboard.
        If there are any errors in sending the message to either user
        (e.g., if they have blocked or deleted the bot), then those errors are ignored.

    :param st: Send a message to the developer and admin
    :param keyboard: Send a custom keyboard to the user
    :return: The keyboard
    """
    try:
        await bot.send_message(DEVELOPER_ID, st, reply_markup=keyboard)
    except Exception:
        pass
    try:
        if DEVELOPER_ID != ADMIN_ID:
            await bot.send_message(ADMIN_ID, st, reply_markup=keyboard)
    except Exception:
        pass
    await asyncio.sleep(1)
