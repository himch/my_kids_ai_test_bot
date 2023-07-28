# -----------------------------------------------------------
# https://t.me/my_kids_ai_test_bot Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# ----------------------------------------------------------

from aiogram import executor
from misc import dp
import handlers


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


