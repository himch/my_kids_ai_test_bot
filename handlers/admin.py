# -----------------------------------------------------------
# admin panel for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# -----------------------------------------------------------

from aiogram import types
from aiogram.dispatcher import FSMContext

from dbase import dbase
from misc import dp
from utils import print_user_list, admin_only


#######################################################################################################################
# admin commands
#######################################################################################################################
@admin_only
@dp.message_handler(commands="admin", state="*")
async def cmd_admin(message: types.Message, state: FSMContext):
    await message.answer("Список команд для админа:\n" +
                         "/all_users - список всех пользователей\n" +
                         "/delete_all_users - удалить всех пользователей\n\n" +
                         "/change_pic - поменять картинку\n\n" +
                         "/start - вернуться в пользовательское меню",
                         reply_markup=types.ReplyKeyboardRemove())


@admin_only
@dp.message_handler(commands="all_users", state="*")
async def cmd_all_users(message: types.Message, state: FSMContext):
    await message.answer("Список пользователей:",
                         reply_markup=types.ReplyKeyboardRemove())
    await print_user_list(message, dbase.get_all_users(), 0)
    await message.answer("Нажмите /admin для списка команд админа", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(None)


@admin_only
@dp.message_handler(commands="delete_all_users", state="*")
async def cmd_delete_all_users(message: types.Message, state: FSMContext):
    dbase.delete_all_users()
    await message.answer("Готово", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(None)


@admin_only
@dp.message_handler(commands="change_pic", state="*")
async def cmd_change_pic(message: types.Message, state: FSMContext):
    await message.answer(
        "Просто пришли сюда картинку", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(None)


@admin_only
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message, state: FSMContext):
    # admin zone - load new start pic
    await message.photo[-1].download('pic.jpg')
    await message.answer("Готово, картинка заменена")
    await state.set_state(None)

