# -----------------------------------------------------------
# messages panel for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# -----------------------------------------------------------

messages = {}
messages['start_message'] = ('Привет, [user] ❤️\n\n'
                             'Добро пожаловать в мой бот.\n'
                             'Он написан на языке Python.\n'
                             'Чтобы посмотреть его исходный код, используй команду /github.\n'
                             'Чтобы попасть в меню служебных команд, используй команду /admin (если у тебя есть доступ 😏).\n'
                             'Все остальные возможности доступны через кнопочное меню.\n\n'
                             '⚠️ Если кнопочное меню скрыто, нажми иконку 🎛 в правом нижнем углу')
messages["not_admin"] = "Вас нет в списке администраторов. Обратитесь в техническую поддержку"
messages["select_media"] = "Выберите медиаконтент"
messages["about"] = "About"
messages["github"] = "Исходный код проекта можно найти в этом репозитарии: "