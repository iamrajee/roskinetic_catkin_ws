#include <ArduinoHardware.h>
#include <ros.h>
#include <geometry_msgs/Twist.h>

#define LEFT_MOTOR_1   48
#define LEFT_MOTOR_2   49
#define LEFT_MOTOR_PWM 6
#define RIGHT_MOTOR_PWM 5
#define RIGHT_MOTOR_1   46
#define RIGHT_MOTOR_2   47

ros::NodeHandle nh;
int lowSpeed = 220;
int highSpeed = 30;

void messageCb( const geometry_msgs::Twist& msg){
  
   if(msg.angular.z>0)
   {
      moveLeft();
   }
   else if(msg.angular.z<0)
   {
      moveRight();
   }
   else if(msg.angular.z == 0)
   {
      moveFront();
   }
}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", &messageCb );



void setup()
{
  pinMode(LEFT_MOTOR_1, OUTPUT);
  pinMode(LEFT_MOTOR_2, OUTPUT);
  pinMode(LEFT_MOTOR_PWM, OUTPUT);
  pinMode(RIGHT_MOTOR_PWM, OUTPUT);
  pinMode(RIGHT_MOTOR_1, OUTPUT);
  pinMode(RIGHT_MOTOR_2, OUTPUT);

 //initialization of motors

  digitalWrite(RIGHT_MOTOR_1, LOW);
  digitalWrite(RIGHT_MOTOR_2, LOW);
  digitalWrite(RIGHT_MOTOR_1, LOW);
  digitalWrite(RIGHT_MOTOR_2, LOW);
  
  analogWrite(RIGHT_MOTOR_PWM, lowSpeed);
  analogWrite(RIGHT_MOTOR_PWM, lowSpeed); 
  nh.initNode();
  nh.subscribe(sub);
} 

void loop()
{
 nh.spinOnce();
 delay(20);
 }
void moveLeft(){
  
  digitalWrite(LEFT_MOTOR_1, LOW);
  digitalWrite(LEFT_MOTOR_2, HIGH);
  digitalWrite(RIGHT_MOTOR_1, LOW);
  digitalWrite(RIGHT_MOTOR_2, HIGH);
  
  analogWrite(LEFT_MOTOR_PWM, lowSpeed);
  analogWrite(RIGHT_MOTOR_PWM, highSpeed);  
  
  delay(1500);
  moveFront();
  
}

void moveFront(){
  
  digitalWrite(LEFT_MOTOR_1, LOW);
  digitalWrite(LEFT_MOTOR_2, HIGH);
  digitalWrite(RIGHT_MOTOR_1, LOW);
  digitalWrite(RIGHT_MOTOR_2, HIGH);
  
  analogWrite(LEFT_MOTOR_PWM, highSpeed);
  analogWrite(RIGHT_MOTOR_PWM, highSpeed);
  
}

void moveRight(){
  
  digitalWrite(LEFT_MOTOR_1, LOW);
  digitalWrite(LEFT_MOTOR_2, HIGH);
  digitalWrite(RIGHT_MOTOR_1, LOW);
  digitalWrite(RIGHT_MOTOR_2, HIGH);
  
  analogWrite(LEFT_MOTOR_PWM, highSpeed);
  analogWrite(RIGHT_MOTOR_PWM, lowSpeed);
  
  delay(1500);
  moveFront();
  
}
