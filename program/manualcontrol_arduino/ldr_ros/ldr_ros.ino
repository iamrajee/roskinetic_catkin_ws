#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <ros.h>
#include <std_msgs/UInt16.h>

ros::NodeHandle  nh;

#define ldr_pin A0

std_msgs::UInt16 ldr_msg;
ros::Publisher ldrpub("ldr", &ldr_msg);
void setup(){
  pinMode(ldr_pin, INPUT);
  nh.initNode();
  nh.advertise(ldrpub);
 }

void loop(){
  ldr_msg.data = analogRead(ldr_pin);
  ldrpub.publish( &ldr_msg );
  nh.spinOnce();
  delay(1000);
}
