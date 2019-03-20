#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <ArduinoHardware.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>

Servo servo;
#define lm_en 2
#define rm_en 3
#define lm1   22
#define lm2   23
#define rm1   24
#define rm2   25
#define servo_pin 9

ros::NodeHandle nh;
//int lowSpeed = 220;
//int highSpeed = 30;
int Speed = 120;
int lSpeed = Speed;
int rSpeed = Speed;

void servo_cb( const std_msgs::UInt16& cmd_msg){
  servo.write(cmd_msg.data); //set servo angle, should be from 0-180  
  digitalWrite(13, HIGH-digitalRead(13));  //toggle led
  delay(cmd_msg.data*15);
}

void velsubCB( const geometry_msgs::Twist& vel){

   if(vel.linear.x == 0 && vel.angular.z == 0)
   {
      Stop();
   } else {
      if(vel.linear.x>0)
      {
          forward();
      }
      else if(vel.linear.x<0)
      {
          backward();
      }
      
      if(vel.angular.z>0)
      {
          sleft();
      }
      else if(vel.angular.z<0)
      {
          sright();
      }
   }
   
}

void lSpeed_cb( const std_msgs::UInt16& msg){
  lSpeed = msg.data;
  analogWrite(lm_en, lSpeed);
}
void rSpeed_cb( const std_msgs::UInt16& msg){
  rSpeed = msg.data;
  analogWrite(rm_en, rSpeed);
}
void Speed_cb( const std_msgs::UInt16& msg){
  Speed = msg.data;
  lSpeed = Speed;
  rSpeed = Speed;
  analogWrite(lm_en, lSpeed);
  analogWrite(rm_en, rSpeed);
}
ros::Subscriber<geometry_msgs::Twist> velsub("/teleop/turtlebot_teleop/cmd_vel", &velsubCB );
ros::Subscriber<std_msgs::UInt16> Speedsub("/Speed", Speed_cb );
ros::Subscriber<std_msgs::UInt16> lSpeedsub("/Speed/lSpeed", &lSpeed_cb);
ros::Subscriber<std_msgs::UInt16> rSpeedsub("/Speed/rSpeed", &rSpeed_cb);
ros::Subscriber<std_msgs::UInt16> servosub("servo", servo_cb);

void setup()
{

  nh.initNode();
  nh.subscribe(velsub);
  nh.subscribe(Speedsub);
  nh.subscribe(lSpeedsub);
  nh.subscribe(rSpeedsub);
  nh.subscribe(servosub);

  servo.attach(servo_pin);
  
  pinMode(13, OUTPUT);
  pinMode(lm1, OUTPUT);
  pinMode(lm2, OUTPUT);
  pinMode(lm_en, OUTPUT);
  pinMode(rm1, OUTPUT);
  pinMode(rm2, OUTPUT);
  pinMode(rm_en, OUTPUT);

 //initialization of motors

  digitalWrite(lm1, 0);
  digitalWrite(lm2, 0);
  digitalWrite(rm1, 0);
  digitalWrite(rm2, 0);
  
  analogWrite(lm_en, 0);
  analogWrite(rm_en, 0); 
} 

void loop()
{
 nh.spinOnce();
 delay(1);
}
void setmotor(int lm1_v,int lm2_v,int rm1_v, int rm2_v){
  digitalWrite(lm1, lm1_v);
  digitalWrite(lm2, lm2_v);
  digitalWrite(rm1, rm1_v);
  digitalWrite(rm2, rm2_v);
  analogWrite(lm_en, lSpeed);
  analogWrite(rm_en, rSpeed);
}
void forward(){
  setmotor(1,0,1,0);
}
void backward(){
  setmotor(0,1,0,1);
}
void left(){
  setmotor(0,1,1,0);
}
void right(){
  setmotor(1,0,0,1); 
}
void sleft(){
  setmotor(0,0,1,0);
}
void sright(){
  setmotor(1,0,0,0);
}
void Stop(){
  setmotor(0,0,0,0);
  analogWrite(lm_en, 0);
  analogWrite(rm_en, 0);
}
