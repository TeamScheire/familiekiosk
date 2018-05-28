# -*- coding: utf-8 -*-
"""
Created on Sun May 27 12:14:12 2018

@author: benny
"""

# you need: https://pypi.org/project/RPi.GPIO/ 
# install via: sudo apt-get install python-rpi.gpio python3-rpi.gpio
import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)

#use pin 17 to query the pushbutton
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(17)
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.2)
