"""
keyboards for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

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
    """
    The get_media_submenu_commands function returns a ReplyKeyboardMarkup object with buttons for each file in the
    media_type directory. The media_type argument is a string that specifies which type of media to display,
    and can be one of 'voice', 'audio', 'video', or 'photo'.
    Each button has the sub_menu_btn symbol prepended to its caption, so that it can be
    distinguished from other types of buttons.

    :param media_type: Specify the type of media to be sent
    :return: A list of buttons for the submenu
    """
    submenu = ReplyKeyboardMarkup(resize_keyboard=True)
    try:
        items = os.listdir(os.path.join(FILES_DIRECTORY, media_type))
    except FileNotFoundError:
        items = []
    for btn_caption in items:
        submenu.add(KeyboardButton(sub_menu_btn_symbol + btn_caption))
    submenu.add(KeyboardButton(back_btn))
    return submenu
