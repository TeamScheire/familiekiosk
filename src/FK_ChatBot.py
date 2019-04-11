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

from __future__ import division, print_function

import sys, os.path

if sys.version_info[0] == 2:  # the configparser library changed it's name from Python 2 to 3.
    import ConfigParser
    configparser = ConfigParser
else:
    import configparser
    
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, Job, BaseFilter)
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


ACCEPTED_CHATS = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])), 'chatlist.ini')
APPROVED_CHATS = []

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hallo, geef het wachtwoord in met commando \n/secret XXXXX\n (XXXX vervang je door het wachtwoord)')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(bot, update):
    """Echo the user message."""
    print ('tekst')
    sys.stdout.flush()
    update.message.reply_text(update.message.text)

def secret(bot, update, args):
    """Give the secret to accept messages to this bot """
    global APPROVED_CHATS
    password = "".join(args)
    print ('Received pass', password)
    sys.stdout.flush()
    if password == PASSWORD:
        update.message.reply_text("Correct! Vanaf nu kan je foto's en video's sturen naar deze groep")
        #we voegen toe aan lijst van correcte chat
        chatid = update.message.chat.id
        print (chatid)
        sys.stdout.flush()
        
        if os.path.isfile(ACCEPTED_CHATS):
            config = ConfigParser.RawConfigParser()
            config.read(ACCEPTED_CHATS)
            try:
                chat_idtxt = config.get("Approved", "chatids")
            except:
                chat_idtxt = ""
            chat_ids = chat_idtxt.split(',')
            APPROVED_CHATS = [int(x) for x in chat_ids if x]
            if chatid and chatid not in APPROVED_CHATS:
                #add it to accepted chatids
                APPROVED_CHATS += [chatid]
                if not config.has_option("Approved", "chatids"):
                    config.add_section("Approved")
                config.set("Approved", "chatids",
                           ','.join([str(x) for x in APPROVED_CHATS]))
                with open(ACCEPTED_CHATS, 'wb') as metafile:
                    config.write(metafile)
    else:
        update.message.reply_text("Fout wachtwoord!")
        
def not_authorized(bot, update):
    update.message.reply_text('Je bent nog niet gekend, geef eerst het wachtwoord in met commando \n/secret XXXXX\n (XXXX vervang je door het wachtwoord)')

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


class FilterApprovedChat(BaseFilter):
    def filter(self, message):
        return message.chat.id in APPROVED_CHATS

# Remember to initialize the class.
filter_approved_chats = FilterApprovedChat()

def main():
    """Start the bot."""
    # Obtain approved chats
    global APPROVED_CHATS
    if os.path.isfile(ACCEPTED_CHATS):
        config = ConfigParser.RawConfigParser()
        config.read(ACCEPTED_CHATS)
        try:
            chat_idtxt = config.get("Approved", "chatids")
        except:
            chat_idtxt = ""
        chat_ids = chat_idtxt.split(',')
        APPROVED_CHATS = [int(x) for x in chat_ids if x]
            
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("secret", secret, pass_args=True))
    
    # For testing: on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.all, echo))

    # we react on receiving a picture
    dp.add_handler(MessageHandler(Filters.photo & filter_approved_chats, picturehandler.on_photo_received))
    # we react on receiving an voice message
    dp.add_handler(MessageHandler(Filters.voice & filter_approved_chats, voicehandler.on_voice_received))
    dp.add_handler(MessageHandler(Filters.video_note & filter_approved_chats, videohandler.on_video_note_received))
    dp.add_handler(MessageHandler(Filters.video & filter_approved_chats, videohandler.on_video_received))

    # catchall if not approved user
    dp.add_handler(MessageHandler(Filters.photo | Filters.voice | Filters.video_note | Filters.video, not_authorized))
    
    # Get the job queue to shedule jobs, see doc at
    # https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-JobQueue
    jq = updater.job_queue
    
    # scan if we need to reply from time to time (every 2 min)
    job_reply = jq.run_repeating(do_reply, interval=120, first=0)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(poll_interval=5, timeout=10)

    print ('fk_chatbot started')
    sys.stdout.flush()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    #some blabla to update chmod
    main()
