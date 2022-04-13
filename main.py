#!/usr/bin/env python
# pylint: disable=C0116,W0613

import os
import logging
from dotenv import dotenv_values

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

config = {
    **dotenv_values(".env"),
    **os.environ
}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Введи номер для получения ссылки")

def make_link(update: Update, context: CallbackContext) -> None:
    array = [int(s) for s in list(update.message.text) if s.isdigit()]
    numbers = ''.join(str(x) for x in array)
    if len(numbers[-10:]) != 10:
        update.message.reply_text("Проверь правильность номера")
        return
    update.message.reply_text("wa.me/7" + numbers[-10:])

def main() -> None:
    updater = Updater(config['TOKEN'])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", start))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, make_link))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
