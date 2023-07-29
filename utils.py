# -----------------------------------------------------------
# utils for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# ----------------------------------------------------------

import asyncio
from aiogram import types

from config import DEVELOPER_ID, ADMIN_ID
from dbase import dbase
from misc import bot


async def get_user_data(data, message):
    data['db_tgid'] = message.from_user.id
    data['db_full_name'] = message.from_user.full_name
    return dbase.add_user(data['db_tgid'], message.chat.id)


async def print_user(tg_id, print_tg_id=True):
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
    """Generate and print clickable Telegram user list."""
    if users and len(users) > 0:
        for row in users:
            await message.answer(await print_user(row[row_index]),
                                 reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Нет таких, список пуст",
                             reply_markup=types.ReplyKeyboardRemove())


async def send_info_to_dev_admin(st, keyboard=None):
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
