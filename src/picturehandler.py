# -*- coding: utf-8 -*-

#Adapted From
# https://github.com/zeroone2numeral2/nmjpeg-bot/blob/master/modules/compressor.py

import os
import sys
import logging
import datetime
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

EMAIL = ""
#sending mail info 
# note: required install: sudo apt-get install ssmtp 
UserName = "YOUR_GMAIL_ACCOUNT@gmail.com"
UserPassword = "YOUR_GMAIL_PASSWORD"
SmptPort = 587  # google: 465
SmptServer = 'smtp.gmail.com' #localhost' # google: 'smtp.gmail.com'

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

    def send(self):
        with open(self.compressed_file_path, 'rb') as file:
            #we reply in telegram with the photo as feedback
            self.message.reply_photo(file, reply_to_message_id=self.reply_to_message_id)
            #we send to photo frame email
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
def on_photo_received(bot, update):
    logger.info("photo received")

    quality_level = 50 # 100 is full best quality, 1 is worst

    PictureExtended(update.message, quality=quality_level).download_send2frame()

#some test code
def test_email():
    send_mail("/home/benny/git/familiekiosk/src/pics/-248259759_62_comp.jpg")
    
if __name__ == '__main__':
    test_email();
