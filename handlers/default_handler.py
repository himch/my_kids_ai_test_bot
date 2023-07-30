"""
default handlers for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

from misc import dp
from aiogram import types


#####################################################################################################################
# default
#####################################################################################################################

@dp.message_handler(content_types=types.ContentTypes.ANY, state="*")
async def all_other_messages(message: types.Message):
    """
    The all_other_messages function is a default handler for all messages that are not handled by any other handlers.
    It replies to the user with &quot;Ничего не понимаю!&quot;
    if the message content type is text, and &quot;Зачем тут это?&quot; otherwise.

    :param message: types.Message: Pass the message object to the function
    :return: A message that the bot does not understand
    """
    if message.content_type == types.ContentTypes.TEXT:
        await message.reply("Ничего не понимаю!")
    else:
        await message.reply("Зачем тут это?")
