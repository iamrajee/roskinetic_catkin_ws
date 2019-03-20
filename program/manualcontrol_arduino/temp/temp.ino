#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <ros.h>
#include <std_msgs/Float64.h>

// defines pins numbers
#define temp_pin A4

ros::NodeHandle nh;

//Publiser
std_msgs::Float64 temp_msg;
ros::Publisher temppub("temp",&temp_msg);

// defines variables
float temp;

//Subscriber

void setup() {
  nh.initNode();
  imusetup();
}

void loop() {
  imuloop();
  nh.spinOnce();
}
void imusetup(){
  nh.advertise(temppub);
  pinMode(temp_pin, OUTPUT);
}
void imuloop(){
  temp_msg.data=analogRead(temp_pin)*0.48828125;
  temppub.publish(&temp_msg);
}
