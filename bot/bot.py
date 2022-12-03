

def main():
    updater = Updater(creds.TG_BOT_TOKEN, persistence=storage)
    dispatcher = updater.dispatcher

    updater.start_polling()
    updater.idle()
