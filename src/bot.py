"""This file contains realization of CD_MBot"""

import os
import time
import traceback
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from yt_dlp import YoutubeDL
from yt_dlp.postprocessor.common import PostProcessor

from src.strings import *


class FilenameCatcher(PostProcessor):
    """Class contains postprocessor that catches cache filenames"""

    def __init__(self):
        super(FilenameCatcher, self).__init__(None)
        self.filenames = []

    def run(self, information):
        self.filenames.append(information["filepath"])
        return [], information


class Form(StatesGroup):
    """Bot FSM Class"""

    lang = State()
    loop = State()
    search = State()


class MBot(Bot):
    """Class contains CD_Mbot"""

    dispatcher: Dispatcher = None
    __storage: MemoryStorage = None
    __conf: dict = None
    __locale: StringsLang = StringsEn

    def __init__(self, token: str, conf: dict):
        super().__init__(token)

        logging.basicConfig(filename=os.path.join(conf['Logger']['logdir'], 'log.log'),
                            encoding='utf-8',
                            level=logging.INFO)

        self.__conf = conf

        self.__storage = MemoryStorage()

        self.dispatcher = Dispatcher(self, storage=self.__storage)
        self.dispatcher.register_message_handler(self.__start, state='*', commands=['start'])
        self.dispatcher.register_message_handler(self.__handle_lang_keyboard, state=Form.lang)
        self.dispatcher.register_message_handler(self.__help, state=Form.loop, commands=['help'])
        self.dispatcher.register_message_handler(self.__search, state=Form.loop, commands=['search'])
        self.dispatcher.register_message_handler(self.__lang, state=Form.loop, commands=['lang'])
        self.dispatcher.register_message_handler(self.__handle_loop_keyboard, state=Form.loop)
        self.dispatcher.register_message_handler(self.__perform_search, state=Form.search)

    async def __start(self, message: types.Message) -> None:
        """Message handler for /start"""
        logging.info(f'Received \'/start\' from user {message.from_user.id}')

        try:
            await Form.lang.set()
            logging.info(f'User {message.from_user.id} state set to \'lang\'')

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(StringsLang.str_en, StringsLang.str_ru)

            await self.send_message(message.from_user.id, self.__locale.str_greeting, reply_markup=markup)
        except Exception:
            logging.error(traceback.format_exc())
            await self.send_message(message.from_user.id, self.__locale.str_error_internal)
            print(traceback.format_exc())

    async def __help(self, message: types.Message) -> None:
        """Message handler for /help"""
        logging.info(f'Received \'/help\' from user {message.from_user.id}')

        try:
            await self.send_message(message.from_user.id, self.__locale.str_help_content)
        except Exception:
            logging.error(traceback.format_exc())
            await self.send_message(message.from_user.id, self.__locale.str_error_internal)
            print(traceback.format_exc())

    async def __search(self, message: types.Message) -> None:
        """Message handler for /search"""
        logging.info(f'Received \'/search\' from user {message.from_user.id}')

        await Form.search.set()
        logging.info(f'User {message.from_user.id} state set to \'search\'')

        await self.send_message(message.from_user.id, self.__locale.str_search_request)

    async def __lang(self, message: types.Message) -> None:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(StringsLang.str_en, StringsLang.str_ru)

        logging.info(f'Received \'/lang\' from user {message.from_user.id}')

        await Form.lang.set()
        logging.info(f'User {message.from_user.id} state set to \'lang\'')
        await self.send_message(message.from_user.id, self.__locale.str_lang_choose, reply_markup=markup)

    async def __perform_search(self, message: types.Message) -> None:
        """Message handler for user search request"""

        try:
            track_name = message.text
            ydl = YoutubeDL(self.__conf['YDL'])

            await self.send_message(message.from_user.id, self.__locale.str_search_start)

            filename_collector = FilenameCatcher()
            ydl.add_post_processor(filename_collector)
            video_info = ydl.extract_info(f"ytsearch:{track_name}", download=True)['entries'][0]

            await message.reply_document(open(filename_collector.filenames[0], 'rb'),
                                         caption=f'\U0001F3B5 \n{video_info["title"]}\n\U0001F3B5')
            await self.send_message(message.from_user.id, self.__locale.str_search_end)

            time.sleep(5)
            os.remove(filename_collector.filenames[0])
        except Exception:
            logging.error(traceback.format_exc())
            await self.send_message(message.from_user.id, self.__locale.str_error_internal)
            print(traceback.format_exc())

        await Form.loop.set()
        logging.info(f'User {message.from_user.id} state set to \'loop\'')

    async def __handle_lang_keyboard(self, message: types.message) -> None:
        """Message handler for user lang change request"""

        try:
            locale = message.text

            if locale in locales.keys():
                self.__locale = locales[locale]
            else:
                await self.send_message(message.from_user.id, self.__locale.str_error_not_found)
                return

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(self.__locale.str_search, self.__locale.str_help, self.__locale.str_lang)

            await self.send_message(message.from_user.id, self.__locale.str_greeting_lang, reply_markup=markup)

        except Exception:
            logging.error(traceback.format_exc())
            await self.send_message(message.from_user.id, self.__locale.str_error_internal)
            print(traceback.format_exc())

        await Form.loop.set()
        logging.info(f'User {message.from_user.id} state set to \'loop\'')

    async def __handle_loop_keyboard(self, message: types.Message) -> None:
        """Message handler for buttons"""

        match str(message.text):
            case self.__locale.str_search:
                logging.info(f'Received \'/search\' from user {message.from_user.id}')

                await Form.search.set()
                await self.send_message(message.from_user.id, self.__locale.str_search_request)

            case self.__locale.str_help:
                await self.__help(message)

            case self.__locale.str_lang:
                await self.__lang(message)

            case _:
                await self.send_message(message.from_user.id, self.__locale.str_error_not_found_help)
