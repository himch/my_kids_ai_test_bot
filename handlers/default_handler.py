# -----------------------------------------------------------
# default handlers for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# ----------------------------------------------------------

from misc import dp
from aiogram import types


#####################################################################################################################
# default
@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def all_other_messages(message: types.Message):
    """Default handler"""
    if message.content_type == "text":
        await message.reply("Ничего не понимаю!")
    else:
        await message.reply("Зачем тут это?")