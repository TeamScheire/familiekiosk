#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

from config import *

HAS_BUTTON = REPLY_BUTTON or NEXT_BUTTON or PREV_BUTTON
HAS_GPIO = HAS_BUTTON or BUZZER_PRESENT

STATE_PIC = 0
STATE_VID = 1
STATE_AUD = 2

TEST_VID = True

import os
import sys

import pexpect   # sudo apt-get install python-pexpect
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter

import threading

if sys.version_info[0] == 2:  # the configparser library changed it's name from Python 2 to 3.
    import ConfigParser
    configparser = ConfigParser
else:
    import configparser

from PIL import Image, ImageTk
import time
from datetime import datetime

# you need: https://pypi.org/project/RPi.GPIO/ 
# install via: sudo apt-get install python-rpi.gpio python3-rpi.gpio
if HAS_GPIO:
    import RPi.GPIO as GPIO

import glob

import gi
gi.require_version('Gst', '1.0')      # install with: sudo apt-get install python-gst-1.0 gstreamer1.0-tools
gi.require_version('GstVideo', '1.0')
gi.require_version('GdkX11', '3.0')
from gi.repository import Gst, GObject, GdkX11, GstVideo


BASE_PIC_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/pics/'
IMAGES = os.path.join(BASE_PIC_PATH, '*.jpg')

BASE_VID_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/video/'
VIDEOS = os.path.join(BASE_VID_PATH, '*.mp4')

BASE_AUD_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/voice/'
VOICES = os.path.join(BASE_AUD_PATH, '*.ogg')

testvid = BASE_VID_PATH + "/dummy/testvideo.mp4"
testaud = BASE_AUD_PATH + "/dummy/testvoice.ogg"


class TVbox():
        
    def __init__(self):
        self.state = STATE_PIC
        self.change_state = False
        self.timeticks = 200
        self.timeslept = 0
        
        self.currentimage = -1
        self.currentvideo = -1
        self.currentaudio = -1
        self.showimagenr = 0
        self.showvideonr = 0
        self.showaudionr = 0
        self.len_img_list = 0
        self.len_vid_list = 0
        self.len_aud_list = 0
        self.list_of_img = []
        self.list_of_vid = []
        self.list_of_aud = []
        self.timeshowstart = time.time()
        self.replybtnpressed = False
        self.nextbtnpressed = False
        self.prevbtnpressed = False
        self.stopplayingvideo = False
        self.stopplayingaudio = False
        self.ext_process = None
        
        self.root = tkinter.Tk()
        #self.root.attributes('-fullscreen', True)
        #set no border
        self.root.config(highlightthickness=0, cursor='none')
        self.label = tkinter.Label(text="Foto van ...", font=("Courier", 44))
        self.label.pack(fill=tkinter.X)
        
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.bind('<Escape>', self.closefullscreen)
        self.root.bind('<Return>', self.closefullscreen)
        self.root.bind("<ButtonPress-1>", self.closefullscreen)
        self.root.bind("<ButtonPress-2>", self.test_prev)
        self.root.bind("<ButtonPress-3>", self.test_next)
        self.root.overrideredirect(True)
        # no window decoration to close the window! 
        self.root.geometry("%dx%d+0+0" % (self.w, self.h))
        self.root.resizable(False, False)
        self.root.update_idletasks()
        self.root.focus_set()
        
        #update Tk to be able to querry label size
        self.root.update()
        self.w_label, self.h_label = self.label.winfo_width(), self.label.winfo_height()
        
        # add a canvas
        self.canvas = tkinter.Canvas(self.root, width=self.w, height=self.h-self.h_label, bg="black",
                                     highlightthickness=0)
        #canvas.configure(background='black')
        #canvas.bind("<Escape>", closefullscreen)
        #canvas.bind("<Return>", closefullscreen)
        self.canvas.bind("<ButtonPress-1>", self.closefullscreen)
        self.canvas.bind("<ButtonPress-2>", self.test_prev)
        self.canvas.bind("<ButtonPress-3>", self.test_next)
        
        # set up the reply button
        if HAS_GPIO:
            GPIO.setmode(GPIO.BCM)
        if REPLY_BUTTON:
            #use pin 18 to query the pushbutton
            GPIO.setup(REPLY_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if NEXT_BUTTON:
            #use pin 18 to query the pushbutton
            GPIO.setup(NEXT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if PREV_BUTTON:
            #use pin 23 to query the pushbutton
            GPIO.setup(PREV_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if BUZZER_PRESENT:
            GPIO.setup(BUZZER_PIN, GPIO.OUT)

        self.canvas.pack()
        
        # add gstreamer now in it's own canvas
        
        GObject.threads_init()
        Gst.init(None)
        
        # you can also use display_frame = tkinter.Frame(window)
        self.display_frame = tkinter.Canvas(self.root, width=self.w, height=self.h-self.h_label,
                                            bg="black", highlightthickness=0)
        self.display_frame.bind("<ButtonPress-1>", self.closefullscreen)
        self.display_frame.bind("<ButtonPress-2>", self.test_prev)
        self.display_frame.bind("<ButtonPress-3>", self.test_next)
        self.display_frame.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
        self.frame_id = self.display_frame.winfo_id()

        self.listimages()
        self.listvideos()
        self.listvoices()
        
        if (TEST_VID):
            self.state = STATE_VID
            self.change_state = True

        self.show()
        
        #start with pics only     
        #self.hide_vid()
        
        self.update_app()
        
        self.root.mainloop()


    def set_frame_handle(self, bus, message):
        if not message.get_structure() is None:
            #print (message.get_structure().get_name())
            if message.get_structure().get_name() == 'prepare-window-handle':
                display_frame = message.src
                display_frame.set_property('force-aspect-ratio', True)
                display_frame.set_window_handle(self.frame_id)

    def show_pic(self):
        self.canvas.pack()
    
    def hide_pic(self):
        self.canvas.pack_forget()
        
    def show_vid(self):
        self.display_frame.pack(side=tkinter.TOP, expand=tkinter.YES, fill=tkinter.BOTH)
        self.frame_id = self.display_frame.winfo_id()    
        
    def hide_vid(self):
        self.display_frame.pack_forget()

    def set_video(self, path):
        filepath = os.path.realpath(path)
        filepath2 = "file:///" + filepath.replace('\\', '/').replace(':', '|')
        self.player.set_property('uri', filepath2)

    def most_recent_mode(self):
        """
        In recent mode or not? recent mode is from Alarm to Alarm + 30 min
        """
        if (TEST_VID): return True
        #30 min after alarm time only recent images
        now = datetime.now()
        limit_min_start = ALARM_HOUR * 60 + ALARM_MIN
        limit_min_end = limit_min_start + 30
        now_min = now.hour *60 + now.minute
        #print (limit_min_start, now_min, limit_min_end)
        # limit pics if needed
        if limit_min_start <= now_min <= limit_min_end:
            return True
        return False

    def listimages(self):
        """
        Obtain a list of images to allow reaction
        30 min after alarm time: only the recent images
        otherwise all images
        """
        list_of_files = sorted( glob.iglob(IMAGES), key=os.path.getmtime, reverse=True)
    
        list_of_files = [x for x in list_of_files if x[-9:] != "_comp.jpg"]
        if self.len_img_list != len(list_of_files):
            #new image arrived, show it
            self.showimagenr = 0
        self.len_img_list = len(list_of_files)
        
        if self.most_recent_mode():
            self.list_of_img = list_of_files[:MAX_JPG]
        else:
            self.list_of_img = list_of_files
        #print (self.list_of_img)

    def listvideos(self):
        """
        Obtain a list of videos to allow reaction
        30 min after alarm time: only the recent videos
        otherwise all videos
        """
        list_of_files = sorted( glob.iglob(VIDEOS), key=os.path.getmtime, reverse=True)
    
        if self.len_vid_list != len(list_of_files):
            #new video arrived, show it
            self.showvideonr = 0
        self.len_vid_list = len(list_of_files)
        
        if self.most_recent_mode():
            self.list_of_vid = list_of_files[:MAX_VID]
        else:
            self.list_of_vid = list_of_files

    def listvoices(self):
        """
        Obtain a list of voice messages to allow reaction
        30 min after alarm time: only the recent videos
        otherwise all videos
        """
        list_of_files = sorted( glob.iglob(VOICES), key=os.path.getmtime, reverse=True)
    
        if self.len_aud_list != len(list_of_files):
            #new video arrived, show it
            self.showaudionr = 0
        self.len_aud_list = len(list_of_files)
        
        if self.most_recent_mode():
            self.list_of_aud = list_of_files[:MAX_AUD]
        else:
            self.list_of_aud = list_of_files

    def show(self):
        """ update what we show """
        # first stop playing something if needed
        if self.stopplayingaudio or (self.stopplayingvideo and not USE_EXTERNAL_VIDEO_PLAYER):
            #stop gstreamer
            if hasattr(self, 'player'):
                print ('STOPPING the current playing track on gstreamer')
                self.player.set_state(Gst.State.READY)
                self.player.set_state(Gst.State.NULL)
                del self.bus
                del self.player
        elif self.stopplayingvideo and USE_EXTERNAL_VIDEO_PLAYER:
            # we need to kill the subprocess running the external vid ...
            if self.ext_process:
                #self.ext_process.kill()
                # to kill omxplayer only sending CTRL-C seems to work:
                self.ext_process.sendcontrol('c')
                self.ext_process.close()
                time.sleep(0.2)
                self.ext_process = None
            
        if not self.most_recent_mode():
            #we should only show pictures! 
            if self.state != STATE_PIC:
                self.state = STATE_PIC
                self.change_state = False
                self.hide_vid()
                self.show_pic()
        
        #depending on state, we show pic, video or voice
        if self.state == STATE_PIC:
            self.showimage()
        elif self.state == STATE_VID:
            self.showvideo()
        elif self.state == STATE_AUD:
            self.showvoice()
                            
    def showimage(self):
        if self.currentimage != self.showimagenr:
            # we regenerate list of images to have latest present
            self.listimages()
            # now show the next image
            if len(self.list_of_img) == 0 :
                #no images yet, show dummy
                self.showPIL(os.path.join(BASE_PIC_PATH, 'dummy', 'dummy.jpg'))
                meta_filename = None
            else:
                self.showimagenr = self.showimagenr % len(self.list_of_img)
                self.showPIL(self.list_of_img[self.showimagenr])
                meta_filename = self.list_of_img[self.showimagenr] + '_meta.cfg'
            self.timeshowstart = time.time()
            self.currentimage = self.showimagenr
            #obtain meta information if present
            if meta_filename and os.path.isfile(meta_filename):
                config = ConfigParser.RawConfigParser()
                config.read(meta_filename)
                self.img_user = "{} {}".format(config.get("user", "first_name"),
                                           config.get("user", "last_name"))
                self.img_day = config.get("message", "day")
            else:
                self.img_user = ''
                self.img_day = ''

    def showPIL(self, image_file):
        pilImage = Image.open(image_file)
        imgWidth, imgHeight = pilImage.size
        print ('SHOWING', image_file, imgWidth, imgHeight, self.w, self.h-self.h_label)
        # too large or too small, scale to fit the frame
        ratio = min(self.w/imgWidth, (self.h-self.h_label)/imgHeight)
        imgWidth = int(imgWidth*ratio)
        imgHeight = int(imgHeight*ratio)
        pilImage = pilImage.resize((imgWidth, imgHeight), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(pilImage)
        imagesprite = self.canvas.create_image(self.w/2, 
                                               (self.h-self.h_label)/2, 
                                               image=self.image)

    def showvideo(self):
        if self.currentvideo != self.showvideonr:
            # we regenerate list of vids to have latest present
            self.listvideos()
            # now show the next image
            if len(self.list_of_vid) == 0 :
                #no vid yet, ERROR ! 
                return

            self.showvideonr = self.showvideonr % len(self.list_of_vid)

            if USE_EXTERNAL_VIDEO_PLAYER:
                self.ext_process = pexpect.spawn('omxplayer ' +
                                        self.list_of_vid[self.showvideonr]) 
            else:
                #show video
                if hasattr(self, 'player'):
                    del self.bus
                    del self.player
                self.player = Gst.ElementFactory.make('playbin', None)
                self.bus = self.player.get_bus()
                self.bus.enable_sync_message_emission()
                self.bus.connect('sync-message::element', self.set_frame_handle)
                self.set_video(self.list_of_vid[self.showvideonr])
                self.player.set_state(Gst.State.PLAYING)

            self.timeshowstart = time.time()
            meta_filename = self.list_of_vid[self.showvideonr] + '_meta.cfg'
            self.currentvideo = self.showvideonr
            #obtain meta information if present
            if meta_filename and os.path.isfile(meta_filename):
                config = ConfigParser.RawConfigParser()
                config.read(meta_filename)
                self.img_user = "{} {}".format(config.get("user", "first_name"),
                                           config.get("user", "last_name"))
                self.img_day = config.get("message", "day")
                self.playduration = config.getfloat("message", "duration") + 3
            else:
                self.img_user = ''
                self.img_day = ''
                self.playduration = 10

    def showvoice(self):
        if self.currentaudio != self.showaudionr:
            # we regenerate list of vids to have latest present
            self.listvoices()
            # now show the next image
            if len(self.list_of_aud) == 0 :
                #no vid yet, ERROR ! 
                return

            self.showaudionr = self.showaudionr % len(self.list_of_aud)
            print('playing', self.showaudionr, self.list_of_aud[self.showaudionr])

            if True:
                #play audio
                if hasattr(self, 'player'):
                    del self.bus
                    del self.player
                self.player = Gst.ElementFactory.make('playbin', None)
                self.bus = self.player.get_bus()
                self.bus.enable_sync_message_emission()
                self.bus.connect('sync-message::element', self.set_frame_handle)
                self.set_video(self.list_of_aud[self.showaudionr])
                self.player.set_state(Gst.State.PLAYING)
                
            self.timeshowstart = time.time()
            meta_filename = self.list_of_aud[self.showaudionr] + '_meta.cfg'
            self.currentaudio = self.showaudionr
            #obtain meta information if present
            if meta_filename and os.path.isfile(meta_filename):
                config = ConfigParser.RawConfigParser()
                config.read(meta_filename)
                self.img_user = "{} {}".format(config.get("user", "first_name"),
                                           config.get("user", "last_name"))
                self.img_day = config.get("message", "day")
                self.playduration = config.getfloat("message", "duration") + 3
            else:
                self.img_user = ''
                self.img_day = ''
                self.playduration = 10

    def btn_pressed(self, pin):
        """
        Determine if the reply button is pressed. Return True if pressed
        """
        if HAS_BUTTON:
            return GPIO.input(pin)
        else:
            return False

    def is_do_reply(self):
        """
        We send reply if the reply button is released.
        This returns True if this is the case, False otherwise
        """
        if not REPLY_BUTTON:
            return False
        
        if self.btn_pressed(REPLY_PIN) and not self.replybtnpressed:
            self.replybtnpressed = True
            #time.sleep(0.1)
            return False
        
        if self.replybtnpressed and not self.btn_pressed(REPLY_PIN):
            # button released
            self.replybtnpressed = False
            return True
        
        return False

    def test_next(self, event):
        self.nextbtnpressed = True
        
    def test_prev(self, event):
        self.prevbtnpressed = True

    def is_do_next(self):
        """
        We do next if the next button is released.
        This returns True if this is the case, False otherwise
        """
        if not NEXT_BUTTON:
            # 3rd mouse button via test_next might have been used
            if self.nextbtnpressed:
                self.nextbtnpressed = False
                return True
            return False
        
        if self.btn_pressed(NEXT_PIN) and not self.nextbtnpressed:
            self.nextbtnpressed = True
            #time.sleep(0.1)
            return False
        
        if self.nextbtnpressed and not self.btn_pressed(NEXT_PIN):
            # button released
            self.nextbtnpressed = False
            return True
        
        return False

    def is_do_prev(self):
        """
        We do prev if the prev button is released.
        This returns True if this is the case, False otherwise
        """
        if not PREV_BUTTON:
            # 2rd mouse button via test_prev might have been used
            if self.prevbtnpressed:
                self.prevbtnpressed = False
                return True
            return False
        
        if self.btn_pressed(PREV_PIN) and not self.prevbtnpressed:
            self.prevbtnpressed = True
            #time.sleep(0.1)
            return False
        
        if self.prevbtnpressed and not self.btn_pressed(PREV_PIN):
            # button released
            self.prevbtnpressed = False
            return True
        
        return False

    def do_reply(self):
        """
        We send via telegram a chat that we like this image
        """
        print ("Replying to the shown image or video")
        if ((self.state == STATE_PIC and len(self.list_of_img) == 0) or
           (self.state == STATE_VID and len(self.list_of_vid) == 0) or
           (self.state == STATE_AUD and len(self.list_of_aud) == 0)) :
            #nothing to reply to
            return
        # obtain user that send the image
        if (self.state == STATE_PIC):
            ourlist = self.list_of_img
            current = self.currentimage
        elif (self.state == STATE_VID):
            ourlist = self.list_of_vid
            current = self.currentvideo
        elif (self.state == STATE_AUD):
            # we don't reply to audio msg
            ourlist = self.list_of_aud
            current = self.currentaudio
        else:
            return
            
        meta_filename = ourlist[current] + '_meta.cfg'
        #obtain meta information if present
        if os.path.isfile(meta_filename):
            config = ConfigParser.RawConfigParser()
            config.read(meta_filename)
            if config.get("message", "chat_id"):
                #indicate to the chat bot to send a reply to this picture
                dirn, basen = os.path.split(meta_filename)
                print ("Chat present, preparing reply on", basen)
                reply_filename = os.path.join(dirn, 'reply', basen)
                with open(reply_filename, 'wb') as replyfile:
                    replyfile.write("reply")
            else:
                print ("No chat id, no reply.", meta_filename)
        else:
            print ("No meta file, no reply.", meta_filename)

    def do_alarm(self):
        alarm_on = False
        # default: no alarm
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        now = datetime.now()
        # do 1 minute alarm
        if now.hour == ALARM_HOUR:
            if now.minute == ALARM_MIN:
                if now.second % 6 < 3:
                    alarm_on = True
        if alarm_on:
            #do on for 50 ms
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.05)
            self.timeslept += 50
            GPIO.output(BUZZER_PIN, GPIO.HIGH)

    def update_app(self):
        """
        Scheduled function running every second
        """
        self.timeslept = 0
        # test if reply button pressed
        if self.is_do_reply():
            self.do_reply()
        
        # update the label, show new image if needed
        now = time.strftime("%H:%M:%S")
        doprev = self.is_do_prev()
        donext = self.is_do_next()
        self.stopplayingvideo = False
        self.stopplayingaudio = False
        if self.state == STATE_PIC:
            if self.change_state:
                self.hide_vid()
                self.show_pic()
                self.change_state = False
            # update image if needed
            if (doprev):
                if self.showimagenr > 0:
                    self.showimagenr -= 1
                else:
                    self.showimagenr = len(self.list_of_img) - 1
                    if self.most_recent_mode(): 
                        #change state to voice if messages
                        self.change_state = True
                        if len(self.list_of_aud):
                            self.state = STATE_AUD
                        elif len(self.list_of_vid):
                            self.state = STATE_VID
                self.show()
            elif (donext or time.time() > self.timeshowstart + SHOW_JPG_SEC):
                self.showimagenr += 1
                self.showimagenr = self.showimagenr % len(self.list_of_img)
                if (self.most_recent_mode() and self.showimagenr % len(self.list_of_img) == 0):
                    self.change_state = True
                    if len(self.list_of_vid):
                        self.state = STATE_VID
                    elif len(self.list_of_aud):
                        self.state = STATE_AUD
                self.show()
        elif self.state == STATE_VID:
            if self.change_state:
                self.hide_pic()
                self.show_vid()
                
            if (doprev):
                self.stopplayingvideo = True
                if self.showvideonr > 0:
                    self.showvideonr -= 1
                else:
                    self.showvideonr = len(self.list_of_vid) - 1
                    if self.most_recent_mode(): 
                        #change state to pic
                        self.change_state = True
                        self.state = STATE_PIC
                self.show()
            elif (donext or time.time() > self.timeshowstart + self.playduration):
                if donext:
                    self.stopplayingvideo = True
                self.showvideonr += 1
                self.showvideonr = self.showvideonr % len(self.list_of_vid)
                if (self.most_recent_mode() and self.showvideonr % len(self.list_of_vid) == 0):
                    self.change_state = True
                    if len(self.list_of_aud):
                        self.state = STATE_AUD
                    else:
                        self.state = STATE_PIC
                self.show()
        
        elif self.state == STATE_AUD:
            if self.change_state:
                self.hide_pic()
                self.hide_vid()
                
            if (doprev):
                self.stopplayingaudio = True
                if self.showaudionr > 0:
                    self.showaudionr -= 1
                else:
                    self.showaudionr = len(self.list_of_aud) - 1
                    if self.most_recent_mode(): 
                        if len(self.list_of_vid):
                            self.state = STATE_VID
                        else:
                            self.state = STATE_PIC
                self.show()
            elif (donext or time.time() > self.timeshowstart + self.playduration):
                if donext:
                    self.stopplayingaudio = True
                self.showaudionr += 1
                self.showaudionr = self.showaudionr % len(self.list_of_aud)
                if (self.most_recent_mode() and self.showaudionr % len(self.list_of_aud) == 0):
                    self.change_state = True
                    self.state = STATE_PIC
                self.show()
                
        txt = "{} - {} ({})".format(now, self.img_user, self.img_day)
        self.label.configure(text=txt)
        
        # check time to see if we need to do alarm
        if BUZZER_PRESENT and ALARM_SET:
            self.do_alarm()       
        
        self.root.after(200-self.timeslept, self.update_app)
        
    def closefullscreen(self, event):
        #master.withdraw() # if you want to bring it back
        print ("In close fullscreen")
        if BUZZER_PRESENT:
            #switch off
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            
        self.root.destroy()
        #event.widget.withdraw()
        #event.widget.quit()
        #sys.exit() # if you want to exit the entire thing

    
if __name__ == '__main__':
    app = TVbox()