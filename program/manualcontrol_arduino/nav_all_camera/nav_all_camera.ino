/*********** HARDWARE ***********/
#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif
/*********** INCLUDE ***********/
#include <ArduinoHardware.h>
#include <ros.h>
#include <ros/time.h>
#include <geometry_msgs/Twist.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>

/*********** PIN ***********/
/* LED */
#define led_pin 13
/* SERVO */
Servo camera_servo;
#define camera_servo_pin 6
/* MOTOR */
#define Flm_en 2
#define Frm_en 3
#define Flm1   46
#define Flm2   47
#define Frm1   48
#define Frm2   49
#define Blm_en 4
#define Brm_en 5
#define Blm1   50
#define Blm2   51
#define Brm1   52
#define Brm2   53

/*********** VARIABLE ***********/
int lowSpeed = 130;
int highSpeed = 255;
int Speed = 120;
int FSpeed = Speed;
int BSpeed = 150;
int FlSpeed = FSpeed;
int FrSpeed = FSpeed;
int BlSpeed = BSpeed;
int BrSpeed = BSpeed;

long toggleled_time;

/*********** CALLBACK ***********/
void camera_servo_cb( const std_msgs::UInt16& cmd_msg){
  camera_servo.write(cmd_msg.data); //set servo angle, should be from 0-180
  delay(cmd_msg.data*15);
}
void cmd_vel_cb( const geometry_msgs::Twist& vel){
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
          left();
      }
      else if(vel.angular.z<0)
      {
          right();
      }
   }  
}
void lSpeed_cb( const std_msgs::UInt16& msg){
  FlSpeed = msg.data;
  BlSpeed = msg.data;
  analogWrite(Flm_en, FlSpeed);
  analogWrite(Blm_en, BlSpeed);
}
void rSpeed_cb( const std_msgs::UInt16& msg){
  FrSpeed = msg.data;
  BrSpeed = msg.data;
  analogWrite(Frm_en, FrSpeed);
  analogWrite(Brm_en, BrSpeed);
}
void Speed_cb( const std_msgs::UInt16& msg){
  FlSpeed = msg.data;
  BlSpeed = msg.data;
  FrSpeed = msg.data;
  BrSpeed = msg.data;
  analogWrite(Flm_en, FlSpeed);
  analogWrite(Blm_en, BlSpeed);
  analogWrite(Frm_en, FrSpeed);
  analogWrite(Brm_en, BrSpeed);
}

/*********** NODE ***********/
ros::NodeHandle nh;
/*********** PUBLISHER ***********/
/*********** SUBSCRIBER ***********/
ros::Subscriber<geometry_msgs::Twist> cmd_vel_sub("/teleop/turtlebot_teleop/cmd_vel", &cmd_vel_cb);
ros::Subscriber<std_msgs::UInt16> Speed_sub("/Speed", Speed_cb );
ros::Subscriber<std_msgs::UInt16> lSpeed_sub("/Speed/lSpeed", &lSpeed_cb);
ros::Subscriber<std_msgs::UInt16> rSpeed_sub("/Speed/rSpeed", &rSpeed_cb);
ros::Subscriber<std_msgs::UInt16> camera_servo_sub("servo", camera_servo_cb);

/***************** MAIN SETUP *******************/
void setup()
{
  nh.initNode();
  led_setup();
  cmd_vel_setup();
  camera_servo_setup();
}
/***************** OTHER SETUP *******************/
void led_setup(){
  pinMode(led_pin, OUTPUT);
  digitalWrite(led_pin, 0);
  toggleled_time =  millis();
}
void cmd_vel_setup()
{
  nh.subscribe(cmd_vel_sub);
  nh.subscribe(Speed_sub);
  nh.subscribe(lSpeed_sub);
  nh.subscribe(rSpeed_sub);
  /* FRONT MOTOR */
  pinMode(Flm1, OUTPUT);
  pinMode(Flm2, OUTPUT);
  pinMode(Flm_en, OUTPUT);
  pinMode(Frm1, OUTPUT);
  pinMode(Frm2, OUTPUT);
  pinMode(Frm_en, OUTPUT);
  //initialization of motors
  digitalWrite(Flm1, 0);
  digitalWrite(Flm2, 0);
  digitalWrite(Frm1, 0);
  digitalWrite(Frm2, 0);
  analogWrite(Flm_en, 0);
  analogWrite(Frm_en, 0);
  /* BACK MOTOR */
  pinMode(Blm1, OUTPUT);
  pinMode(Blm2, OUTPUT);
  pinMode(Blm_en, OUTPUT);
  pinMode(Brm1, OUTPUT);
  pinMode(Brm2, OUTPUT);
  pinMode(Brm_en, OUTPUT);
  //initialization of motors
  digitalWrite(Blm1, 0);
  digitalWrite(Blm2, 0);
  digitalWrite(Brm1, 0);
  digitalWrite(Brm2, 0);
  analogWrite(Blm_en, 0);
  analogWrite(Brm_en, 0);
}
void camera_servo_setup()
{
  nh.subscribe(camera_servo_sub);
  camera_servo.attach(camera_servo_pin);
  camera_servo.write(90);
  delay(1000);
}

/***************** MAIN LOOP *******************/
void loop()
{
 nh.spinOnce();
 led_loop();
 //delay(1);
}
/***************** OTHER LOOP *******************/
/***************** HELPER FUNCTION ****************/
void led_loop(){
  if ( millis() - toggleled_time >=1000)
 {
    digitalWrite(led_pin, HIGH-digitalRead(13));  //toggle led
    toggleled_time =  millis();   
 }
}
/*================ CMD_VEL_HELPER ==============*/
void setmotor(int lm1_v,int lm2_v,int rm1_v, int rm2_v){
  /* FRONT MOTOR */
  digitalWrite(Flm1, lm1_v);
  digitalWrite(Flm2, lm2_v);
  digitalWrite(Frm1, rm1_v);
  digitalWrite(Frm2, rm2_v);
  analogWrite(Flm_en, FlSpeed);
  analogWrite(Frm_en, FrSpeed);
  /* BACK MOTOR */
  digitalWrite(Blm1, lm1_v);
  digitalWrite(Blm2, lm2_v);
  digitalWrite(Brm1, rm1_v);
  digitalWrite(Brm2, rm2_v);
  analogWrite(Blm_en, BlSpeed);
  analogWrite(Brm_en, BrSpeed);
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
  analogWrite(Flm_en, 0);
  analogWrite(Frm_en, 0);
  analogWrite(Blm_en, 0);
  analogWrite(Brm_en, 0);
}
