# -----------------------------------------------------------
# main menu for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# -----------------------------------------------------------

import os
from datetime import datetime
import soundfile as sf

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import ContentType

from audio_speech_recognition import recognizer
from config import FILES_DIRECTORY, MY_LOCATION, DEVELOPER_ID
from keyboards import main_menu_keyboard, photo_btn, video_btn, voice_btn, posts_btn, back_btn, \
    about_btn, sub_menu_btn_symbol, get_media_submenu_commands, speech_recognition_btn
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
            await send_info_to_dev_admin(st)
        media = types.InputFile('pic.jpg')
        await message.answer_photo(media, reply_markup=main_menu_keyboard)
        await message.answer(messages['start_message'].replace("[user]",
                                                               await print_user(message.from_user.id,
                                                                                print_tg_id=False)),
                             reply_markup=main_menu_keyboard)
        await state.set_state(None)


@dp.message_handler(Text(equals=[photo_btn, video_btn, voice_btn, posts_btn]), state="*")
async def cmd_select_media_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['db_media_type'] = message.text
        await message.answer(messages["select_media"],
                             reply_markup=get_media_submenu_commands(message.text))
        await state.set_state(None)


@dp.message_handler(Text(startswith=sub_menu_btn_symbol), state="*")
async def cmd_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        filename = message.text[2:]
        path = os.path.join(FILES_DIRECTORY, data['db_media_type'], filename)
        if data['db_media_type'] == photo_btn:
            media = types.InputFile(path)
            await message.answer_photo(media, caption=filename)
        elif data['db_media_type'] == video_btn:
            media = types.InputFile(path)
            await message.answer_video(media, caption=filename)
        elif data['db_media_type'] == voice_btn:
            media = types.InputFile(path)
            await message.answer_voice(media, caption=filename)
        elif data['db_media_type'] == posts_btn:
            with open(path) as f:
                lines = f.readlines()
                await message.answer(f'<b>{filename}</b>\n\n' + ''.join(lines))
        else:
            await message.answer(messages["something_wrong"] )
        await state.set_state(None)


@dp.message_handler(commands="about", state="*")
@dp.message_handler(Text(equals=about_btn), state="*")
async def cmd_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(messages["about"].replace("[user]", await print_user(DEVELOPER_ID, print_tg_id=False)),
                             reply_markup=main_menu_keyboard)
        await message.answer_location(*MY_LOCATION)
        await state.set_state(None)


@dp.message_handler(commands="github", state="*")
async def cmd_github(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(messages["github"],
                             reply_markup=main_menu_keyboard)
        await state.set_state(None)


@dp.message_handler(Text(equals=speech_recognition_btn), state="*")
async def cmd_select_media_type(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await message.answer(messages["voice_commands"])
        await state.set_state(None)
        # await state.set_state(StatesLoadVoiceCommand.wait_for_voice_command)


@dp.message_handler(content_types=ContentType.VOICE)
async def handle_wait_for_voice_command(message: types.Message, state: FSMContext):
    # admin zone - load and run voice command
    async with state.proxy() as data:
        filename = str(datetime.now()).translate(str.maketrans({' ': '_', ':': '-', '.': '_'}))
        path = os.path.join(FILES_DIRECTORY, filename)
        await message.voice.download(destination_file=path + '.ogg', make_dirs=True)
        data, samplerate = sf.read(path + '.ogg')
        sf.write(path + '.wav', data, samplerate)
        await message.answer("Звуковое загружено, идет распознование...")
        text = recognizer.recognize(path + '.wav')
        if text:
            await message.answer(f"Распознана команда <b>{text}</b>, пытаюсь выполнить...")
            if text == 'start':
                await cmd_start(message, state)
            elif text == 'github':
                await cmd_github(message, state)
            elif text == 'about':
                await cmd_about(message, state)
            else:
                await message.answer("Такая команда не поддерживается!")
        else:
            await message.answer(messages["something_wrong"] )
        await state.set_state(None)


#####################################################################################################################
# назад
#####################################################################################################################

@dp.message_handler(Text(equals=back_btn, ignore_case=True), state="*")
async def cmd_back(message: types.Message, state: FSMContext):
    """Return to main menu."""
    async with state.proxy() as data:
        await message.answer("Продолжим?", reply_markup=main_menu_keyboard)
    await state.set_state(None)
