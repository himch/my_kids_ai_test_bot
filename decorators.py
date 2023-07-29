# -----------------------------------------------------------
# decorators for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# ----------------------------------------------------------

from decorator import decorator

from dbase import user_is_admin
from messages import messages


@decorator
async def admin_only(coro, *args):
    admin = await user_is_admin(*args)
    if not admin:
        await args[0].answer(messages["not_admin"])
        return True
    return await coro(*args)
