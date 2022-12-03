

def main():
    updater = Updater(creds.TG_BOT_TOKEN)
    dispatcher = updater.dispatcher

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()