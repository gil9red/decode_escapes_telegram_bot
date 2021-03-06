#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext, Defaults

from config import TOKEN
from common import get_logger, log_func, reply_error
from utils import decode


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.effective_message.reply_text(
        'Бот для декодирования последовательностей вида &#x20AC; &#8364; &euro;'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message
    message.reply_text(
        decode(message.text),
        quote=True
    )


def on_error(update: Update, context: CallbackContext):
    reply_error(log, update, context)


def main():
    log.debug('Start')

    cpu_count = os.cpu_count()
    workers = cpu_count
    log.debug(f'System: CPU_COUNT={cpu_count}, WORKERS={workers}')

    # Create the EventHandler and pass it your bot's token.
    updater = Updater(
        TOKEN,
        workers=workers,
        defaults=Defaults(run_async=True),
    )

    bot = updater.bot
    log.debug(f'Bot name {bot.first_name!r} ({bot.name})')

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start))
    dp.add_handler(MessageHandler(Filters.text, on_request))

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            log.exception('')

            timeout = 15
            log.info(f'Restarting the bot after {timeout} seconds')
            time.sleep(timeout)
