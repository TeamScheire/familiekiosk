#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Bot to reply to Telegram messages.

This program is dedicated to the public domain under the CC0 license.

This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          Job)
import logging

from config import *

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

import picturehandler
picturehandler.set_email(EMAIL_FRAME)
from replyhandler import do_reply
import voicehandler
import videohandler

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    
    # For testing: on noncommand i.e message - echo the message on Telegram
#    dp.add_handler(MessageHandler(Filters.text, echo))

    # we react on receiving a picture
    dp.add_handler(MessageHandler(Filters.photo, picturehandler.on_photo_received))
    # we react on receiving an voice message
    dp.add_handler(MessageHandler(Filters.voice, voicehandler.on_voice_received))
    dp.add_handler(MessageHandler(Filters.video_note, videohandler.on_video_note_received))
    dp.add_handler(MessageHandler(Filters.video, videohandler.on_video_received))

    # Get the job queue to shedule jobs, see doc at
    # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
    jq = updater.job_queue
    
    # scan if we need to reply from time to time (every 2 min)
    job_reply = jq.run_repeating(do_reply, interval=120, first=0)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=5, timeout=10)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    #some blabla to update chmod
    main()
