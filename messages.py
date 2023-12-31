"""
messages panel for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

messages = dict()
messages['start_message'] = ('Привет, [user] ❤️\n\n'
                             'Добро пожаловать в мой бот.\n'
                             'Он написан на языке Python.\n'
                             'Чтобы посмотреть его исходный код, используй команду /github.\n'
                             'Чтобы попасть в меню служебных команд, используй команду /admin '
                             '(если у тебя есть доступ 😏).\n'
                             'Все остальные возможности доступны через кнопочное меню.\n\n'
                             '⚠️ Если кнопочное меню скрыто, нажми иконку 🎛 в правом нижнем углу')
messages["not_admin"] = "Вас нет в списке администраторов. Обратитесь в техническую поддержку"
messages["select_media"] = "Выбери медиа"
messages["about"] = ("Бот написан Сергеем Химченко\n\n"
                     "Мой телефон: +79216341327\n"
                     "EMail: skhimchenko@gmail.com\n"
                     f"Телеграм: [user]\n"
                     "Сейчас я нахожусь в городе Санкт-Петербург, Россия")
messages["github"] = "Исходный код проекта можно найти в этом репозитарии: https://github.com/himch/my_kids_ai_test_bot"
messages["admin_commands"] = ("Список команд для админа:\n\n"
                              "/all_users - список всех пользователей\n"
                              "/delete_all_users - удалить всех пользователей\n\n"
                              "/add_photo - добавить фото\n"
                              "/add_video - добавить видео\n"
                              "/add_voice - добавить голосовое\n"
                              "/add_post - добавить пост\n\n"
                              "/test_speech_recognizer - тест подсистемы распознования речи\n\n"
                              "/start - вернуться в пользовательское меню")
messages["admin_tip"] = "Нажми /admin для списка команд админа или /start для возврата в основное меню"
messages["voice_commands"] = ("Попробуй послать боту команду в виде голосового.\n"
                              "Запиши одну из команд (<b>start</b>, <b>github</b>, <b>about</b>) "
                              "в виде голосового и пришли боту. "
                              "Бот попытается распознать команду и выполнит ее в случае успешного распознавания.\n\n"
                              "⚠️ Распознавание производится при помощи Carnegie Mellon University's open-source "
                              "библиотеки PocketSphinx")
messages["something_wrong"] = 'Что-то пошло не так('
