import logging

from telegram.ext import Updater
from telegram import BotCommand

import handlers
import extensions
import config


def main():
    log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)
    extensions.Statistics.init()

    updater = Updater(config.TG_BOT_TOKEN)
    updater.bot.set_my_commands([BotCommand("start", "Запустить бота и узнать состояние")])
    handlers.add_handlers(updater.dispatcher)
    logging.info("Bot start")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
