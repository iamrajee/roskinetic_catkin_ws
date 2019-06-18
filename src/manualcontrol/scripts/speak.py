#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import os
from gtts import gTTS
import sys
import time
from time import *

path = '/home/pi/ros_catkin_ws/src/manualcontrol/scripts/mp3/'

def justsave(input):
        inputstrip = "".join(input.split(' '))
        filename = path + inputstrip + '.mp3'
        tts = gTTS(text=input, lang='hi')
        tts.save(filename)

def simplesaveplay(input):
        inputstrip = "".join(input.split(' '))
        filename = path + inputstrip + '.mp3'
	if os.path.isfile(filename):
        	os.system("sudo mpg123 "+filename)
        else:
                tts = gTTS(text=input, lang='hi')
                tts.save(filename)
                os.system("sudo mpg123 "+filename)

def speak_cb(speak_msg):
	rospy.loginfo(speak_msg.data)
	simplesaveplay(speak_msg.data)
def speak():
    rospy.init_node("speak",anonymous=True)
    rospy.Subscriber("speak", String, speak_cb)
    rospy.spin()

if __name__ == '__main__':
	speak()
