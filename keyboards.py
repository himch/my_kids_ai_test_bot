# -----------------------------------------------------------
# keyboards for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# ----------------------------------------------------------

import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import FILES_DIRECTORY


cancel_btn = "❌ Отмена"
proceed_btn = "✔ Продолжить"
confirm_btn = "✔ Все верно"
back_btn = "⏪ Назад"

photo_btn = "📸 Фото"
video_btn = "📽️ Видео"
voice_btn = "🎤 Войсы"
posts_btn = "📚 Посты"
speech_recognition_btn = "🤖 Голосовые команды"
about_btn = "ℹ️ About"
sub_menu_btn_symbol = "◾ "

main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton(photo_btn))
main_menu_keyboard.insert(KeyboardButton(video_btn))
main_menu_keyboard.add(KeyboardButton(voice_btn))
main_menu_keyboard.insert(KeyboardButton(posts_btn))
main_menu_keyboard.add(KeyboardButton(speech_recognition_btn))
main_menu_keyboard.add(KeyboardButton(about_btn))


def get_media_submenu_commands(media_type):
    submenu = ReplyKeyboardMarkup(resize_keyboard=True)
    try:
        items = os.listdir(os.path.join(FILES_DIRECTORY, media_type))
    except FileNotFoundError:
        items = []
    for btn_caption in items:
        submenu.add(KeyboardButton(sub_menu_btn_symbol + btn_caption))
    submenu.add(KeyboardButton(back_btn))
    return submenu
