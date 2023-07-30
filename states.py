"""
states for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class StatesLoadMedia(StatesGroup):
    wait_for_media_caption = State()
    wait_for_media = State()
