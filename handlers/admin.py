"""
admin panel for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

import os

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
    """
    The cmd_cancel function is used to cancel the current operation.
        Args:
            message (types.Message): The Telegram message object that was sent by the user.
            state (FSMContext): The FSM context object for this conversation, which contains a record of all states
            visited during this conversation and any values stored in them.

    :param message: types.Message: Get the message object
    :param state: FSMContext: Store the state of the conversation
    :return: None
    """
    await message.answer("Отменено", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(messages["admin_tip"])
    await state.set_state(None)


#######################################################################################################################
# admin commands
#######################################################################################################################

@admin_only
@dp.message_handler(commands="admin", state="*")
async def cmd_admin(message: types.Message):
    """
    The cmd_admin function is the first function that a user will see when they enter the admin zone.
    It displays all of the available commands for an admin to use, and then waits for them to select one.

    :param message: types.Message: Get the message object
    :return: A list of admin commands
    """
    await message.answer(messages["admin_commands"], reply_markup=types.ReplyKeyboardRemove())


@admin_only
@dp.message_handler(commands="all_users", state="*")
async def cmd_all_users(message: types.Message, state: FSMContext):
    """
    The cmd_all_users function is used to display all users in the database.
        It is only available for admins, and can be accessed by typing /all_users.
        The function displays a list of all users in the database, with their ids and names.

    :param message: types.Message: Get the message that was sent by the user
    :param state: FSMContext: Store information about the current state of the user
    :return: A list of all users
    """
    await message.answer("Список пользователей:", reply_markup=types.ReplyKeyboardRemove())
    await print_user_list(message, dbase.get_all_users(), 0)
    await message.answer(messages["admin_tip"])
    await state.set_state(None)


@admin_only
@dp.message_handler(commands="delete_all_users", state="*")
async def cmd_delete_all_users(message: types.Message, state: FSMContext):
    """
    The cmd_delete_all_users function deletes all users from the database.
        Args:
            message (types.Message): The incoming Telegram message object that triggered this function call.
            state (FSMContext): The FSM context object for the current user's conversation with our bot, used to
                keep track of what command was last called and where we are in the conversation flow.

    :param message: types.Message: Get the message that was sent by the user
    :param state: FSMContext: Store the state of the conversation
    :return: None
    """
    dbase.delete_all_users()
    await message.answer("Готово", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(messages["admin_tip"])
    await state.set_state(None)


@admin_only
@dp.message_handler(commands=["add_photo", "add_video", "add_voice", "add_post"], state="*")
async def cmd_start_load_new_content(message: types.Message, state: FSMContext):
    """
    The cmd_start_load_new_content function is a coroutine that takes in the message and state parameters.
    The function then awaits for the user to input a caption for their media file, or cancels if they choose to do so.

    :param message: types.Message: Get the message sent by the user
    :param state: FSMContext: Store the state of the conversation
    :return: A string
    :doc-author: Trelent
    """
    await message.answer(f"Введи название {message.text[5:]} или нажми /cancel для отмены",
                         reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(StatesLoadMedia.wait_for_media_caption)


@admin_only
@dp.message_handler(state=StatesLoadMedia.wait_for_media_caption, content_types=ContentType.TEXT)
async def handle_load_media_caption(message: types.Message, state: FSMContext):
    """
    The handle_load_media_caption function is a callback function that handles the user's input when
    the bot is in the StatesLoadMedia.wait_for_media state. It takes two arguments: message and state,
    where message is an instance of types.Message and state is an instance of FSMContext.

    :param message: types.Message: Access the message sent by the user
    :param state: FSMContext: Store the state of the conversation
    :return: None
    """
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
        except FileIsTooBig:
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
