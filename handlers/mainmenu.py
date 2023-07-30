"""
main menu for Telegram bot

(C) 2023 Sergey Khimchenko, St.-Petersburg, Russia
Released under GNU Public License (GPL)
email skhimchenko@gmail.com
"""

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
from misc import dp
from utils import get_user_data, print_user, send_info_to_dev_admin


#######################################################################################################################
# general commands
#######################################################################################################################

@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    """
    The cmd_start function is the first function that a user sees when they start interacting with the bot.
    It greets them and asks for their name, which it then stores in a database. It also sets up some other
    variables that are used throughout the rest of this script.

    :param message: types.Message: Get the message object,
    :param state: FSMContext: Store the state of a user
    :return: The main menu keyboard
    """
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
    """
    The cmd_select_media_type function is a callback function that handles the user's selection of media type.
    It takes in two arguments: message and state. The message argument is an object containing information about the
    message sent by the user, while state is an object containing information about the current conversation with
    the user (i.e., what stage of interaction we are at). The cmd_select_media_type function then uses asyncio
    to create a proxy for data, which contains all relevant information from previous stages of interaction
    with this particular user (i.e., their username and selected media type). It then updates data['db_media']

    :param message: types.Message: Get the message that was sent by the user
    :param state: FSMContext: Store the state of the conversation
    :return: The text of the selected media type
    """
    async with state.proxy() as data:
        data['db_media_type'] = message.text
        await message.answer(messages["select_media"],
                             reply_markup=get_media_submenu_commands(message.text))
        await state.set_state(None)


@dp.message_handler(Text(startswith=sub_menu_btn_symbol), state="*")
async def cmd_answer_media(message: types.Message, state: FSMContext):
    """
    The cmd_answer_media function is used to answer a message with the media file that was requested by the user.
    The function takes two arguments:
        1) message - The Telegram Message object that triggered this command.
        2) state - The FSMContext object for this conversation, which contains data about what media
        type was requested and what filename it has in our database.

    :param message: types.Message: Get the message sent by the user
    :param state: FSMContext: Store the state of the conversation
    :return: The media file with the specified name
    """
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
            await message.answer(messages["something_wrong"])
        await state.set_state(None)


@dp.message_handler(commands="about", state="*")
@dp.message_handler(Text(equals=about_btn), state="*")
async def cmd_about(message: types.Message, state: FSMContext):
    """
    The cmd_about function is a command handler that sends the user information about the bot.
    It also sends a location of where I live, and sets the state to None.

    :param message: types.Message: Get the message that was sent by the user
    :param state: FSMContext: Store the state of the conversation
    :return: The about message
    """
    async with state.proxy() as data:
        await message.answer(messages["about"].replace("[user]", await print_user(DEVELOPER_ID, print_tg_id=False)),
                             reply_markup=main_menu_keyboard)
        await message.answer_location(*MY_LOCATION)
        await state.set_state(None)


@dp.message_handler(commands="github", state="*")
async def cmd_github(message: types.Message, state: FSMContext):
    """
    The cmd_github function is a command handler that sends the user to the GitHub repository for this bot.

    :param message: types.Message: Get the message object
    :param state: FSMContext: Store the state of the user
    :return: The github link of the bot
    """
    async with state.proxy() as data:
        await message.answer(messages["github"],
                             reply_markup=main_menu_keyboard)
        await state.set_state(None)


@dp.message_handler(Text(equals=speech_recognition_btn), state="*")
async def cmd_speech_recognition(message: types.Message, state: FSMContext):
    """
    The cmd_speech_recognition function is a command handler that allows the user to send a voice message
    to the bot, which will then be converted into text and sent back to the user. The function also has an FSMContext
    object as an argument, which allows it to set states for this particular conversation.

    :param message: types.Message: Get the message that was sent by the user
    :param state: FSMContext: Store the state of the conversation
    :return: A message that the bot is waiting for a voice command
    """
    async with state.proxy() as data:
        await message.answer(messages["voice_commands"])
        await state.set_state(None)
        # await state.set_state(StatesLoadVoiceCommand.wait_for_voice_command)


@dp.message_handler(content_types=ContentType.VOICE)
async def handle_wait_for_voice_command(message: types.Message, state: FSMContext):
    """
    The handle_wait_for_voice_command function is a callback function that will be called when the user sends
    a voice message. It will download the voice message, convert it to wav format and try to recognize text from it.
    If recognized text is one of supported commands, then this command will be executed.

    :param message: types.Message: Get the message that was sent by the user
    :param state: FSMContext: Store data during a conversation
    :return: The state of the conversation
    """
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
            await message.answer(messages["something_wrong"])
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
