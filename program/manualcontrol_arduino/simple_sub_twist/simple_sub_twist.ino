#include "ros.h"

#include "geometry_msgs/Twist.h"

float x; 

ros::NodeHandle nh;

void velCallback(  const geometry_msgs::Twist& vel)
{
     x = vel.linear.x - 1.0; // I CAN USE VEL AS I WANT
     //Serial1.println("Hi2");
}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel" , velCallback);

void setup() {
    nh.loginfo("Hi1");
    //Serial1.begin(57600);
     nh.initNode();
     nh.subscribe(sub);
}

void loop() {
     nh.spinOnce();
     delay(10);
}
