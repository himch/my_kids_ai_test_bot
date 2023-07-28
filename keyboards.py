# -----------------------------------------------------------
# keyboards for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# ----------------------------------------------------------

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_btn = "❌ Отмена"
proceed_btn = "✔ Продолжить"
confirm_btn = "✔ Все верно"
back_btn = "⏪ Назад"

photo_btn = "🤳 Фото"
video_btn = "📽️ Видео"
voice_btn = "🎤 Голос"
posts_btn = "📚 Посты"
about_btn = "ℹ️ About"
sub_menu_btn_symbol = "◾ "

main_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu_keyboard.add(KeyboardButton(photo_btn))
main_menu_keyboard.insert(KeyboardButton(video_btn))
main_menu_keyboard.add(KeyboardButton(voice_btn))
main_menu_keyboard.insert(KeyboardButton(posts_btn))
main_menu_keyboard.add(KeyboardButton(about_btn))

categories = {photo_btn: {'Мое последнее селфи': 'selfie',
                          'Мое фото из старшей школы': 'old_photo',
                          'Фото любимых мест': 'places'
                          },
              video_btn: {'Любимая музыка': 'music'
                          },
              voice_btn: {'Голосовое "Что такое GPT"': 'voice_gpt' ,
                          'Голосовое "Разница между SQL и NoSQL"': 'voice_sql',
                          'Голосовое "История первой любви"': 'voice_first_love'
                          },
              posts_btn: {'Пост о моем увлечении': 'hobby'
                          }
              }


submenu_keyboards = {}
category_commands = []
for category in categories:
    submenu_keyboards[category] = ReplyKeyboardMarkup(resize_keyboard=True)
    for btn_caption in categories[category]:
        submenu_keyboards[category].add(KeyboardButton(sub_menu_btn_symbol + btn_caption))
        category_commands.append(categories[category][btn_caption])
    submenu_keyboards[category].add(KeyboardButton(back_btn))