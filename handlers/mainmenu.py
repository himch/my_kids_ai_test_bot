# -----------------------------------------------------------
# main menu for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# -----------------------------------------------------------

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards import main_menu_keyboard, photo_btn, video_btn, voice_btn, posts_btn, submenu_keyboards, back_btn, \
    about_btn, sub_menu_btn_symbol, category_commands
from messages import messages
from misc import dp, bot

from utils import get_user_data, print_user, send_info_to_dev_admin


#######################################################################################################################
# general commands
#######################################################################################################################

@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_added = await get_user_data(data, message)
        if user_added:
            st = "ℹ️ Новый пользователь: " + await print_user(data['db_tgid'])
            await send_info_to_dev_admin(bot, st)
        media = types.InputFile('pic.jpg')
        await message.answer_photo(media, reply_markup=main_menu_keyboard)
        await message.answer(messages['start_message'].replace("[user]", message.from_user.username),
                             reply_markup=main_menu_keyboard)
        await state.set_state(None)


# @dp.message_handler(Text(equals=photo_btn), state="*")
# @dp.message_handler(Text(equals=video_btn), state="*")
# @dp.message_handler(Text(equals=voice_btn), state="*")
@dp.message_handler(Text(equals=[photo_btn, video_btn, voice_btn, posts_btn]), state="*")
async def cmd_select_media_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['db_media_type'] = message.text
        await message.answer(messages["select_media"],
                             reply_markup=submenu_keyboards[message.text])


@dp.message_handler(commands=category_commands, state="*")
@dp.message_handler(Text(startswith=sub_menu_btn_symbol), state="*")
async def cmd_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(message.text)


@dp.message_handler(commands="about", state="*")
@dp.message_handler(Text(equals=about_btn), state="*")
async def cmd_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(messages["about"],
                             reply_markup=main_menu_keyboard)


@dp.message_handler(commands="github", state="*")
async def cmd_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(messages["github"],
                             reply_markup=main_menu_keyboard)


#####################################################################################################################
# отмена
#####################################################################################################################

@dp.message_handler(Text(startswith=back_btn, ignore_case=True), state="*")
async def cmd_back(message: types.Message, state: FSMContext):
    """Return to main menu."""
    async with state.proxy() as data:
        await message.answer("Продолжим?", reply_markup=main_menu_keyboard)
    await state.set_state(None)



