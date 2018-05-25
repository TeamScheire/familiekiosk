#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import sys
if sys.version_info[0] == 2:  # the tkinter library changed it's name from Python 2 to 3.
    import Tkinter
    tkinter = Tkinter #I decided to use a library reference to avoid potential naming conflicts with people's programs.
else:
    import tkinter
from PIL import Image, ImageTk
import time
import glob
import os

MAX_JPG = 20
SHOW_JPG_SEC = 30  # how many seconds to show an image
BASE_FILE_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/pics/'
IMAGES = os.path.join(BASE_FILE_PATH, '*.jpg')

class TVbox():
        
    def __init__(self):
        self.currentimage = -1
        self.showimagenr = 0
        self.timeshowimage = time.time()
        
        self.root = tkinter.Tk()
        #set no border
        self.root.config(highlightthickness=0)
        self.label = tkinter.Label(text="Foto van ...", font=("Courier", 44))
        self.label.pack(fill=tkinter.X)
        
        self.w, self.h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.bind('<Escape>', self.closefullscreen)
        self.root.bind('<Return>', self.closefullscreen)
        self.root.bind("<ButtonPress-1>", self.closefullscreen)
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
        self.canvas.bind("<ButtonPress-3>", self.closefullscreen)
        
        self.listimages()
        self.showimage()
        
        self.canvas.pack()
    
        self.update_label()
        self.root.mainloop()
        
    def listimages(self):
        """
        Obtain a list of last 20 images to allow reaction
        """
        list_of_files = sorted( glob.iglob(IMAGES), key=os.path.getctime, reverse=True)
        list_of_files = [x for x in list_of_files if x[-9:] != "_comp.jpg"]
        self.list_of_img = list_of_files[:MAX_JPG]
        print (self.list_of_img)

    def showimage(self):
        if self.currentimage != self.showimagenr:
            # we regenerate list of images to have latest present
            self.listimages()
            # now show the next image
            if len(self.list_of_img) == 0 :
                #no images yet, show dummy
                self.showPIL(os.path.join(BASE_FILE_PATH, 'dummy', 'dummy.jpg'))
            else:
                self.showimagenr = self.showimagenr % len(self.list_of_img)
                self.showPIL(self.list_of_img[self.showimagenr])
            self.timeshowimage = time.time()
            self.currentimage = self.showimagenr
            

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
        imagesprite = self.canvas.create_image(self.w/2, (self.h-self.h_label)/2, image=self.image)

    def update_label(self):
        """
        Scheduled function running every second
        """
        now = time.strftime("%H:%M:%S")
        self.label.configure(text=now)
        # update image if needed
        if (time.time() > self.timeshowimage + SHOW_JPG_SEC):
            self.showimagenr += 1
            self.showimage()


        self.root.after(1000, self.update_label)
        
        
    def closefullscreen(self, event):
        #master.withdraw() # if you want to bring it back
        print ("In close fullscreen")
        self.root.destroy()
        #event.widget.withdraw()
        #event.widget.quit()
        #sys.exit() # if you want to exit the entire thing

    
if __name__ == '__main__':
    app = TVbox()
