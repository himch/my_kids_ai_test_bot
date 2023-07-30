"""
decorators for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

from decorator import decorator

from dbase import user_is_admin
from messages import messages


@decorator
async def admin_only(coro, *args):
    """
    The admin_only function is a decorator that checks if the user is an admin.
    If they are not, it sends them a message saying so and returns True.
    Otherwise, it calls the coroutine passed to it as an argument.

    :param coro: Pass the function to be executed
    :param *args: Pass a variable number of arguments to the function
    :return: True if the user is not an admin, and false otherwise
    """
    admin = await user_is_admin(*args)
    if not admin:
        await args[0].answer(messages["not_admin"])
        return True
    return await coro(*args)
