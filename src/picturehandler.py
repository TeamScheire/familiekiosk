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
from picture import Picture
# email sending imports
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

BASE_FILE_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/pics/{}_{}.jpg'

from config import *
from libFK import free_Mb

EMAIL = ""

def set_email(email):
    global EMAIL
    EMAIL = email

def get_email():
    return EMAIL

def send_mail(ImgFileName, message=None):
    """Sending a mail with an image from python
        Adapted from https://stackoverflow.com/questions/13070038/attachment-image-to-send-by-mail-using-python
    """
    img_data = open(ImgFileName, 'rb').read()
    msg = MIMEMultipart()
    if message:
         msg['Subject'] = "Foto van {} {} - Datum: {}".format(
                message.from_user.first_name,
                message.from_user.last_name,
                message.date.strftime('%Y-%m-%d %H:%M:%S')
                            )
    else:
         msg['Subject'] = "Nieuw ontvangen foto via Telegram"
    msg['From'] = UserName
    msg['To'] = get_email()
    
    #logger.info(message)

    if message:
        text = MIMEText("Foto van {} {} - Datum: {}".format(
                message.from_user.first_name,
                message.from_user.last_name,
                message.date.strftime('%Y-%m-%d %H:%M:%S')
                            ))
    else:
        text = MIMEText("Nieuw ontvangen foto via Telegram")
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(ImgFileName))
    msg.attach(image)

    s = smtplib.SMTP(SmptServer, SmptPort)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(UserName, UserPassword)
    s.sendmail(UserName, get_email(), msg.as_string())
    s.quit()

class PictureExtended(Picture):
    def __init__(self, message, quality=20):
        if message.reply_to_message:
            self.PhotoSize_object = message.reply_to_message.photo[-1]
            self.reply_to_message_id = message.reply_to_message.message_id
        else:
            self.PhotoSize_object = message.photo[-1]
            self.reply_to_message_id = None

        self.chat_id = message.chat_id
        self.message_id = message.message_id
        self.from_user = message.from_user # user that send the picture
        self.date = message.date # date in Unix time
        self.file_path = BASE_FILE_PATH.format(self.chat_id, self.message_id)
        self.message = message
        Picture.__init__(self, self.file_path, quality=quality)

    def download(self):
        new_file = self.PhotoSize_object.bot.get_file(self.PhotoSize_object.file_id)
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
        with open(self.compressed_file_path, 'rb') as file:
            #we reply in telegram with the photo as feedback
            #self.message.reply_photo(file, reply_to_message_id=self.reply_to_message_id)
            self.message.reply_text('dankjewel voor de foto!')
        if free_Mb() < 80:
            self.message.reply_text("Opgelet, slechts {}Mb vrije ruimte!".format(free_Mb()),
                                reply_to_message_id=self.reply_to_message_id)

        #we send to photo frame email
        if SEND_EMAIL_OF_PICS:
            send_mail(self.compressed_file_path, self.message)

    def download_send2frame(self):
        self.download()
        self.load()
        self.compress()
        self.send()
        #self.remove()

def get_quality_level(args):
    if len(args) > 0:
        try:
            quality_level = int(args[0])
            if quality_level > 99:
                    quality_level = 99
            elif quality_level < 1:
                    quality_level = 1
        except ValueError:
                quality_level = 20
    else:
        quality_level = 20

    return quality_level

@run_async
def on_photo_received(update, args):
    logger.info("photo received")

    quality_level = 80 # 100 is full best quality, 1 is worst
    
    if update and update.message:
        PictureExtended(update.message, quality=quality_level).download_send2frame()

#some test code
def test_email():
    send_mail("/home/benny/git/familiekiosk/src/pics/-248259759_62_comp.jpg")
    
if __name__ == '__main__':
    test_email();
