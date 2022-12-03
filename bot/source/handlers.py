import logging
from functools import wraps
from typing import List

import requests
from telegram.ext import CallbackContext, Dispatcher, CommandHandler, MessageHandler, Filters
from telegram import Update, PhotoSize

import config
import extensions


logger = logging.getLogger(__name__)


def pre_handler(user_data=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            update: Update = args[0]
            context: CallbackContext = args[1]

            user = context.user_data.get(config.SYS_USER_PERSISTENT_KEY)
            if not user:
                context.user_data[config.SYS_USER_PERSISTENT_KEY] = extensions.User()
                extensions.Statistics.register()
                logger.info(f"Register user {update.effective_user.full_name} ({update.effective_user.id})")

            if user_data:
                result = func(*args, user, **kwargs)
            else:
                result = func(*args, **kwargs)

            if update.callback_query:
                update.callback_query.answer()

            return result
        return wrapper
    return decorator


def start(update: Update, context: CallbackContext):
    text = "Добро пожаловать! Просто отправь мне фотографию и я удалю с неё фон."


class PhotoHandler:
    def __init__(self):
        self.tg_handler = MessageHandler(Filters.photo, self.handler)

    @pre_handler(user_data=True)
    def handler(self, update: Update, context: CallbackContext, user: extensions.User):
        extensions.Statistics.use_bot()

        if user.limiter_send_photo.check():
            photos: List[PhotoSize] = update.message.photo
            photo_big = photos[-1]
            photo_content_big = photo_big.get_file().download_as_bytearray()
            response = requests.post(config.URL_DELETE_BACKGROUND, files=photo_content_big)
            if response.ok:
                update.message.reply_photo(response.content)
                user.limiter_send_photo.sent()
            else:
                update.message.reply_text("Что-то пошло не так :(")
                logger.error(f"Error microservice delete background photo: {response.text}")
        else:
            extensions.Statistics.limit_triggered()
            update.message.reply_text(f"Вы отправили слишком много фото. Допустимо {config.COUNT_LIMIT_HANDLER_PHOTO} "
                                      f"фото в {config.TIME_LIMIT_HANDLER_PHOTO / 60} минут.")


def error_handler():
    pass


def add_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(PhotoHandler().tg_handler)
