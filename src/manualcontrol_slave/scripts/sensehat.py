#!/usr/bin/env python

import rospy
from std_msgs.msg import String

import os
import sys
import time
from time import *
import sensehatfunctions
from sensehatfunctions import *

def sensehat_cb(msg):
	#rospy.loginfo(msg.data)
	do = msg.data
	# rotate(180)
	if "red" == do:
		red()
	elif "green" == do:
                green()
        elif "blue" == do:
                blue()
        elif "clear" == do:
                clear()
        elif "front" == do:
                arrow("F")
        elif "left" == do:
                arrow("L")
        elif "right" == do:
                arrow("R")
        elif "back" == do:
                arrow("B")
        elif "smile" == do:
                emoji("smile")
        elif "sad" == do:
                emoji("sad")
        elif "env" == do:
                display_env()
        elif "rainbow" == do:
                rainbow()
        elif "rotate=" in do:
                rotate(int(do.split('=')[1]))
        elif "print=" in do:
                print_text(do.split('=')[1])
        else:
                blue()

def sensehat():
    rospy.init_node("sensehat",anonymous=True)
    rospy.Subscriber("sensehat", String, sensehat_cb)
    rospy.spin()

if __name__ == '__main__':
	try:
		sensehat()
	except:
		clear()
