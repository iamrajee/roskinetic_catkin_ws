#!/usr/bin/env python
import rospy
#from nav_msgs.msg import Odometry
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import motordriver
import time

def move(msg):
    if msg.linear.x == 0 and msg.angular.z == 0:
	motordriver.Stop()
    if msg.linear.x > 0:
	motordriver.forward()
    elif msg.linear.x<0:
	motordriver.backward()
    if msg.angular.z > 0:
        motordriver.sleft()
    elif msg.angular.z<0:
        motordriver.sright()
def callback1(msg):
    rospy.loginfo(msg)
    move(msg)
def callback2(msg):
    rospy.loginfo(msg)
    move(msg)
def main():
    motordriver.forward()
    rospy.init_node("subnav")
    rospy.loginfo("Subscribing to /teleop/turtlebot_teleop/cmd_vel ...")
    rospy.Subscriber("/cmd_vel",Twist,callback1)
    rospy.Subscriber("/teleop/turtlebot_teleop/cmd_vel",Twist,callback2)
    rospy.spin()
if __name__ == '__main__':
    main()
