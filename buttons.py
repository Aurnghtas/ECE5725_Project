'''
ECE5725 Design with Embedded Operating Systems Final Project
author: Jiayi Zhou(jz2372), Bolong Tan(bt362)
'''

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)   # Set for GPIO (bcm) numbering not pin numbers...
# setup piTFT buttons
#                        V need this so that button doesn't 'float'!
#                        V   When button NOT pressed, this guarantees 
#                        V             signal = logical 1 = 3.3 Volts
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def GPIO17_callback(channel):
    print("Button 17 has been pressed")

def GPIO22_callback(channel):
    print("Button 22 has been pressed")

GPIO.add_event_detect(17, GPIO.FALLING, callback=GPIO17_callback, bouncetime=300)
GPIO.add_event_detect(22, GPIO.FALLING, callback=GPIO22_callback, bouncetime=300)

try:
    GPIO.wait_for_edge(27, GPIO.FALLING)
    print("Button 27 has been pressed")
except KeyboardInterrupt:
    GPIO.cleanup() # clean up GPIO on CTRL+C exit

GPIO.cleanup() # clean up GPIO on normal exit
