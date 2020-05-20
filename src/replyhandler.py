# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 15:11:29 2018

@author: benny
"""

import sys
import os.path
import glob


if sys.version_info[0] == 2:  # the configparser library changed it's name from Python 2 to 3.
    import ConfigParser
    configparser = ConfigParser
else:
    import configparser
    ConfigParser = configparser

BASE_FILE_PATH = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])),
                              'pics', 'reply')
REPLIES = os.path.join(BASE_FILE_PATH, '*.jpg_meta.cfg')

REPLY_TEXT = [
    "Mooi!",
    "Geweldig :-)",
    "Leuk dat je aan mij denkt. Bedankt om te delen."
    ]

LAST_REPLY_TEXT = 0

def listreplies():
    """
    Obtain a list of all replies to do
    """
    list_of_files = sorted( glob.iglob(REPLIES), key=os.path.getctime, reverse=False)
    return list_of_files

def do_reply(job):
    """The reply job. This runs every 120 sec and checks if a reply should 
        be posted on a picture
       Added to the jobqueue when chatbot starts
    """
    global LAST_REPLY_TEXT
    # check if there are replies to give and in what chat window   
    for reply2do in listreplies():
        #obtain chat id
        chat_id = ""
        config = None
        dirn, basen = os.path.split(reply2do)
        dirn, _ = os.path.split(dirn[:-1])
        meta_filename = os.path.join(dirn, basen)

        if os.path.isfile(meta_filename):
            config = ConfigParser.RawConfigParser()
            config.read(meta_filename)
            chat_id = config.get("message", "chat_id")
        
        #post a reply
        if chat_id:
            # generate a message for the reply
            reply2use = LAST_REPLY_TEXT
            if config.has_option('reply', 'msgnr'):
                reply2use = (config.getint('reply', 'msgnr') + 1) % len(REPLY_TEXT)
            text = REPLY_TEXT[reply2use]
            msg_text = "{}  -  In antwoord op foto van {} {} op {} {}".format(
                        text,
                        config.get("user", "first_name"),
                        config.get("user", "last_name"),
                        config.get('message', 'day'),
                        config.get('message', 'hour')
                        )
            
            #send the message
            bot.send_message(chat_id=chat_id, text=msg_text)
            #we store the reply done
            if config.has_option('reply', 'msgnr'):
                #we store
                config.set('reply', 'msgnr', reply2use)
            else: 
                config.add_section('reply')
                config.set('reply', 'msgnr', reply2use)
                LAST_REPLY_TEXT = (LAST_REPLY_TEXT + 1) % len(REPLY_TEXT)
            with open(meta_filename, 'wb') as metafile:
                config.write(metafile)

        #now remove the fact we need to do reply as it is done
        os.remove(reply2do)
