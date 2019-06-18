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


// defines pins numbers
Servo lidar_servo;
#define lidar_servo_pin 7
const int trigPin = 40;
const int echoPin = 41;

// defines variables
#define nPoint 90
int flag_sweep,publisher_timer,lidar_servodelay;
long duration;
float time_before,distance;
float ranges[nPoint];

/* NODE */
ros::NodeHandle nh;
//Publiser
sensor_msgs::LaserScan Lidar_msg;
ros:: Publisher lidar_pub("LidarData", &Lidar_msg);

//Subscriber

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
  nh.advertise(lidar_pub);
  flag_sweep = 0;
  lidar_servodelay = 20;
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  lidar_servo.attach(lidar_servo_pin);
  lidar_servo.write(0);
  delay(1000);
  int laser_frequency = 100;
  Lidar_msg.ranges_length = nPoint;
  //Lidar_msg.intensities_length = nPoint;
  Lidar_msg.header.frame_id = "/Lidar_frame";
  Lidar_msg.angle_min = 0.0;
  Lidar_msg.angle_max = 3.14159265;
  Lidar_msg.angle_increment = 3.14159265 / nPoint;
  Lidar_msg.time_increment = 0.200;//((1 /laser_frequency)/nPoint);
  Lidar_msg.range_min = 0.0;
  Lidar_msg.range_max = 3310.0;
  for (int i = 0; i < nPoint; i=i+1) {
       ranges[i]=0.0;
  }
  Lidar_msg.ranges = ranges;
  publisher_timer = millis();
}
void lidarloop(){
  if ((millis() - publisher_timer)> 50 ) 
  {               
    Lidar_msg.header.stamp = nh.now();
    time_before = millis();
    if (flag_sweep == 0){
      for (int theta = 0 ; theta < nPoint; theta++)
      {
        lidar_servo.write(theta*2);
        delay(lidar_servodelay);
        ranges[theta] =  get_ultradist();
        nh.spinOnce();
        //delay(1);
       }
       flag_sweep = 1;
    } else if (flag_sweep == 1){
      for (int theta = nPoint-1 ; theta >= 0; theta--)
      {
        lidar_servo.write(theta*2);
        delay(lidar_servodelay);
        ranges[theta] =  get_ultradist();
        nh.spinOnce();
       }
       flag_sweep = 0;
    }
    Lidar_msg.ranges = ranges;
    Lidar_msg.scan_time = millis() - time_before;
    lidar_pub.publish(&Lidar_msg);
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
