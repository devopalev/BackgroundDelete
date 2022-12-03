from telegram.ext import Updater

import handlers
import config


def main():
    updater = Updater(config.TG_BOT_TOKEN)
    handlers.add_handlers(updater.dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
