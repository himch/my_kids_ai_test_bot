# -----------------------------------------------------------
# admin panel for Telegram bot
#
# (C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
# Released under GNU Public License (GPL)
# email skhimchenko@gmail.com
# -----------------------------------------------------------
import os

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType
from aiogram.utils.exceptions import FileIsTooBig

from audio_speech_recognition import recognizer
from decorators import admin_only
from misc import dp
from config import FILES_DIRECTORY
from dbase import dbase
from keyboards import photo_btn, video_btn, voice_btn, posts_btn
from messages import messages
from states import StatesLoadMedia
from utils import print_user_list


#####################################################################################################################
# отмена
#####################################################################################################################

@admin_only
@dp.message_handler(commands=['cancel'], state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    # admin zone - cancel current operation
    await message.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(messages["admin_tip"])
    await state.set_state(None)


#######################################################################################################################
# admin commands
#######################################################################################################################

@admin_only
@dp.message_handler(commands="admin", state="*")
async def cmd_admin(message: types.Message):
    # admin zone - start message
    await message.answer(messages["admin_commands"], reply_markup=types.ReplyKeyboardRemove())


@admin_only
@dp.message_handler(commands="all_users", state="*")
async def cmd_all_users(message: types.Message, state: FSMContext):
    # admin zone - show all users
    await message.answer("Список пользователей:", reply_markup=types.ReplyKeyboardRemove())
    await print_user_list(message, dbase.get_all_users(), 0)
    await message.answer(messages["admin_tip"])
    await state.set_state(None)


@admin_only
@dp.message_handler(commands="delete_all_users", state="*")
async def cmd_delete_all_users(message: types.Message, state: FSMContext):
    # admin zone - delete all users
    dbase.delete_all_users()
    await message.answer("Готово", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(messages["admin_tip"])
    await state.set_state(None)


@admin_only
@dp.message_handler(commands=["add_photo", "add_video", "add_voice", "add_post"], state="*")
async def cmd_start_load_new_content(message: types.Message, state: FSMContext):
    # admin zone - load new content
    await message.answer(
        f"Введи название {message.text[5:]} или нажми /cancel для отмены", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(StatesLoadMedia.wait_for_media_caption)


@admin_only
@dp.message_handler(state=StatesLoadMedia.wait_for_media_caption, content_types=ContentType.TEXT)
async def handle_load_media_caption(message: types.Message, state: FSMContext):
    # admin zone - load media caption
    async with state.proxy() as data:
        data['admin_media_caption'] = message.text
        await message.answer("Теперь загрузи медиаэлемент или нажми /cancel для отмены",
                             reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(StatesLoadMedia.wait_for_media)


@admin_only
@dp.message_handler(state=StatesLoadMedia.wait_for_media, content_types=ContentType.PHOTO)
async def handle_load_photo(message: types.Message, state: FSMContext):
    # admin zone - load new photo
    async with state.proxy() as data:
        path = os.path.join(FILES_DIRECTORY, photo_btn, data['admin_media_caption'])
        await message.photo[-1].download(destination_file=path, make_dirs=True)
        await message.answer("Готово, фото загружено", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(messages["admin_tip"])
        await state.set_state(None)


@admin_only
@dp.message_handler(state=StatesLoadMedia.wait_for_media, content_types=ContentType.VIDEO)
async def handle_load_video(message: types.Message, state: FSMContext):
    # admin zone - load new photo
    async with state.proxy() as data:
        path = os.path.join(FILES_DIRECTORY, video_btn, data['admin_media_caption'])
        try:
            await message.video.download(destination_file=path, make_dirs=True)
        except FileIsTooBig as e:
            await message.answer("Ошибка FileIsTooBig", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("Готово, видео загружено", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(messages["admin_tip"])
        await state.set_state(None)


@admin_only
@dp.message_handler(state=StatesLoadMedia.wait_for_media, content_types=ContentType.AUDIO)
async def handle_load_voice(message: types.Message, state: FSMContext):
    # admin zone - load new voice
    async with state.proxy() as data:
        path = os.path.join(FILES_DIRECTORY, voice_btn, data['admin_media_caption'])
        await message.audio.download(destination_file=path, make_dirs=True)
        await message.answer("Готово, звуковое загружено", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(messages["admin_tip"])
        await state.set_state(None)


@admin_only
@dp.message_handler(state=StatesLoadMedia.wait_for_media, content_types=ContentType.TEXT)
async def handle_load_post(message: types.Message, state: FSMContext):
    # admin zone - load new post
    async with state.proxy() as data:
        folder = os.path.join(FILES_DIRECTORY, posts_btn)
        if not os.path.exists(folder):
            os.mkdir(folder)
        with open(os.path.join(folder, data['admin_media_caption']), "w", encoding='utf-8') as file:
            file.writelines(message.text)
        await message.answer("Готово, пост загружен", reply_markup=types.ReplyKeyboardRemove())
        await message.answer(messages["admin_tip"])
        await state.set_state(None)


@admin_only
@dp.message_handler(commands="test_speech_recognizer", state="*")
async def cmd_test_speech_recognizer(message: types.Message, state: FSMContext):
    # admin zone - test speech recognizer
    if recognizer.test():
        await message.answer("Подсистема распознования речи в порядке", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Что-то пошло не так", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(messages["admin_tip"])
    await state.set_state(None)
