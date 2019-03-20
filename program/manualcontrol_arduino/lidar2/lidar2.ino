#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h>
#include <ros.h>
#include <ros/time.h>
#include <std_msgs/UInt16.h>
#include <sensor_msgs/LaserScan.h>
#include <math.h>

Servo Rservo;

// defines pins numbers
#define Rservo_pin 10
const int trigPin = 26;
const int echoPin = 27;

ros::NodeHandle nh;

//Publiser
sensor_msgs::LaserScan Laser_msg;
ros:: Publisher laserpub("LaserData", &Laser_msg);

//Subscriber

// defines variables
int flag_sweep,n,publisher_timer,Rservodelay;
long duration;
float time_before,distance;
float ranges[90];

void setup() {
  nh.initNode();
  lidarsetup();
}

void loop() {
  lidarloop();
  nh.spinOnce();
  //delay(100);
}

void lidarsetup()
{ 
  nh.advertise(laserpub);
  flag_sweep = 0;
  n = 90;
  Rservodelay = 20;
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  Rservo.attach(Rservo_pin);
  Rservo.write(0);
  delay(1000);
  int laser_frequency = 100;
  Laser_msg.ranges_length = n;
  //Laser_msg.intensities_length = n;
  Laser_msg.header.frame_id = "/Lidar_frame";
  Laser_msg.angle_min = 0.0;
  Laser_msg.angle_max = 3.14159265;
  Laser_msg.angle_increment = 3.14159265 / n;
  Laser_msg.time_increment = 0.200;//((1 /laser_frequency)/n);
  Laser_msg.range_min = 0.0;
  Laser_msg.range_max = 3310.0;
  for (int i = 0; i < n; i=i+1) {
       ranges[i]=0.0;
  }
  Laser_msg.ranges = ranges;
  publisher_timer = millis();
}
void lidarloop(){
  if ((millis() - publisher_timer)> 50 ) 
  {               
    Laser_msg.header.stamp = nh.now();
    time_before = millis();
    if (flag_sweep == 0){
      for (int theta = 0 ; theta < n; theta++)
      {
        Rservo.write(theta*2);
        delay(Rservodelay);
        ranges[theta] =  get_ultradist();
        nh.spinOnce();
        //delay(1);
       }
       flag_sweep = 1;
    } else if (flag_sweep == 1){
      for (int theta = n-1 ; theta >= 0; theta--)
      {
        Rservo.write(theta*2);
        delay(Rservodelay);
        ranges[theta] =  get_ultradist();
        nh.spinOnce();
       }
       flag_sweep = 0;
    }
    Laser_msg.ranges = ranges;
    Laser_msg.scan_time = millis() - time_before;
    laserpub.publish(&Laser_msg);
    publisher_timer = millis() ;
  }
}
float get_ultradist()
{  
   // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(10);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);//in micro second
  distance= duration*0.034/2;
  return distance;
}
