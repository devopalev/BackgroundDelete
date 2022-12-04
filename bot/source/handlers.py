import logging
from functools import wraps
from typing import List

import requests
from telegram.ext import CallbackContext, Dispatcher, CommandHandler, MessageHandler, Filters, run_async
from telegram import Update, PhotoSize, ParseMode

import config
import extensions

logger = logging.getLogger(__name__)


def pre_handler(user_data=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            def search_arg(arg_class):
                for arg in args:
                    if isinstance(arg, arg_class):
                        return arg

            update: Update = search_arg(Update)
            context: CallbackContext = search_arg(CallbackContext)

            user = context.user_data.get(config.SYS_USER_PERSISTENT_KEY)
            if not user:
                user = context.user_data[config.SYS_USER_PERSISTENT_KEY] = extensions.User()
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


@pre_handler(user_data=False)
def start(update: Update, context: CallbackContext):
    update.effective_chat.send_message("Добро пожаловать! Просто отправь мне фотографию и я удалю с неё фон 😉\n"
                                       f"Изображений в очереди: {extensions.Statistics.get_queue()}\n\n"
                                       'Автор: <a href="https://portfolio.devopalev.ru/">DevOpalev</a>',
                                       parse_mode=ParseMode.HTML)


class PhotoHandler:
    def __init__(self):
        self.tg_handler = MessageHandler(Filters.photo, self.handler)

    @pre_handler(user_data=True)
    def handler(self, update: Update, context: CallbackContext, user: extensions.User):
        try:
            extensions.Statistics.use_bot()

            if user.limiter_send_photo.check():
                photos: List[PhotoSize] = update.message.photo
                photo_big = photos[-1]
                photo_content_big = photo_big.get_file().download_as_bytearray()
                response = requests.post(config.URL_DELETE_BACKGROUND, files={'file': photo_content_big})
                if response.ok:
                    update.message.reply_document(response.content)
                    user.limiter_send_photo.sent()
                else:
                    update.message.reply_text("Что-то пошло не так :(")
                    logger.error(f"Error microservice delete background photo: {response.text}")
            else:
                extensions.Statistics.limit_triggered()
                update.message.reply_text(
                    f"Вы отправили слишком много фото. Допустимо {config.COUNT_LIMIT_HANDLER_PHOTO} "
                    f"фото в {config.TIME_LIMIT_HANDLER_PHOTO / 60} минут.")
        finally:
            extensions.Statistics.del_queue()


def error_handler(update: Update, context: CallbackContext):
    try:
        logger.error(msg="Exception while handling Telegram update:", exc_info=context.error)
        update.effective_chat.send_message("Возникла ошибка :(")
    except Exception as e:
        logger.error(msg="Exception while handling lower-level exception:", exc_info=e)


def add_handlers(dispatcher: Dispatcher):
    dispatcher.add_error_handler(error_handler)
    dispatcher.add_handler(CommandHandler("start", start, run_async=True, ))
    dispatcher.add_handler(PhotoHandler().tg_handler)
