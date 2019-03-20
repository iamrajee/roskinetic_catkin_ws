#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h>
#include <ros.h>
#include <ros/time.h>
#include <sensor_msgs/Imu.h>


// defines pins numbers
#define xpin A1
#define ypin A2
#define zpin A3

ros::NodeHandle nh;

//Publiser
sensor_msgs::Imu imu_msg;
ros::Publisher pub_imu( "/imu", &imu_msg);

//Subscriber

// defines variables
char frameid[] = "/imu";

void setup() {
  nh.initNode();
  imusetup();
}

void loop() {
  imuloop();
  nh.spinOnce();
}

void imusetup()
{ 
  nh.advertise(pub_imu);
  pinMode(xpin,INPUT);
  pinMode(ypin,INPUT);
  pinMode(zpin,INPUT);
  imu_msg.header.frame_id =  "/imu";//frameid;
}
void imuloop(){
  imu_msg.header.stamp=nh.now();
  imu_msg.linear_acceleration.x = analogRead(xpin);
  imu_msg.linear_acceleration.y = analogRead(ypin);
  imu_msg.linear_acceleration.z = analogRead(zpin);
  pub_imu.publish(&imu_msg);
}
