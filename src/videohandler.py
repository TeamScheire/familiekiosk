# -*- coding: utf-8 -*-

#Adapted From
# https://github.com/zeroone2numeral2/nmjpeg-bot/blob/master/modules/compressor.py

import os
import sys
import logging
import datetime

if sys.version_info[0] == 2:  # the configparser library changed it's name from Python 2 to 3.
    import ConfigParser
    configparser = ConfigParser
else:
    import configparser
    ConfigParser = configparser
    
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import BaseFilter
from telegram.ext.dispatcher import run_async

logger = logging.getLogger(__name__)

BASE_FILE_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/video/{}_{}.mp4'

from config import *
from libFK import free_Mb

class VideoExtended():
    def __init__(self, message):
        if message.reply_to_message:
            if  message.reply_to_message.video_note:
                self.VideoNote_object = message.reply_to_message.video_note
            else:
                self.VideoNote_object = message.reply_to_message.video
            self.reply_to_message_id = message.reply_to_message.message_id
        else:
            if  message.video_note:
                self.VideoNote_object = message.video_note
            else:
                self.VideoNote_object = message.video
            self.reply_to_message_id = None

        self.chat_id = message.chat_id
        self.message_id = message.message_id
        self.from_user = message.from_user # user that send the picture
        self.date = message.date # date in Unix time
        self.file_path = BASE_FILE_PATH.format(self.chat_id, self.message_id)
        self.message = message

    def download(self):
        print (self.VideoNote_object)
        duration = self.VideoNote_object.duration
        new_file = self.VideoNote_object.bot.get_file(self.VideoNote_object.file_id,
                                                      timeout=30)
        new_file.download(self.file_path)
        # after saving a file, we need to store some META info also
        meta_info_filename = self.file_path + '_meta.cfg'
        
        meta = configparser.RawConfigParser()
        
        # When adding sections or items, add them in the reverse order of
        # how you want them to be displayed in the actual file.
        meta.add_section('user')
        meta.set('user', 'first_name', self.message.from_user.first_name)
        meta.set('user', 'last_name', self.message.from_user.last_name)
        meta.set('user', 'username', self.message.from_user.username)
        meta.set('user', 'id', self.message.from_user.id)
        meta.add_section('message')
        meta.set('message', 'day', self.message.date.strftime('%Y-%m-%d'))
        meta.set('message', 'hour', self.message.date.strftime('%H:%M:%S'))
        meta.set('message', 'duration', duration)
        if self.message.chat:
            meta.set('message', 'chat_id', self.message.chat.id)
            meta.set('message', 'chat_title', self.message.chat.title)
        else:
            meta.set('message', 'chat_id', '')
            meta.set('message', 'chat_title', '')
        
        # Writing our configuration file
        with open(meta_info_filename, 'w') as metafile:
            meta.write(metafile)

    def send(self):
        self.message.reply_text("Je videobericht is ontvangen", 
                                reply_to_message_id=self.reply_to_message_id)
        if free_Mb() < 80:
            self.message.reply_text("Opgelet, slechts {}Mb vrije ruimte!".format(free_Mb()),
                                reply_to_message_id=self.reply_to_message_id)

    def download_send(self):
        self.download()
        self.send()
        #self.remove()

def on_video_note_received(update, context):
    logger.info("video_note received")
    
    if update and update.message:
        VideoExtended(update.message).download_send()

def on_video_received(update, context):
    logger.info("video received")
    
    if update and update.message:
        VideoExtended(update.message).download_send()

if __name__ == '__main__':
    pass;
