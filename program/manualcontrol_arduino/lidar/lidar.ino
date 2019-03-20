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
//#include <math.h>
#define Rservo_pin 10

ros::NodeHandle nh;
sensor_msgs::LaserScan Laser_msg;

float Angle_min;
float Angle_max;
float Angle_increment;
float Time_increment;
float Scan_time;
float Range_min;
float Range_max;
float Ranges[180]; // max of 90 measurements
float Intensities[180];

int publisher_timer;
int laser_frequency = 100; 
int point_reading = 180;
float time_Now,time_Later;
ros:: Publisher pub_Laser("LaserData", &Laser_msg);
//char frameid[] ="/sonar_ranger";
Servo Rservo;

void setup() 
{
  nh.initNode();
  delay(1000);
  nh.advertise(pub_Laser);
  delay(1000);
 // Serial.begin(57600);
  Angle_min = 0;
  Angle_max = 3.14159265;
  Angle_increment =  3.14159265 / point_reading; //  90 measurement points
  Time_increment=  ((1 /laser_frequency)/point_reading);  // (1 / laser_frequency) / (num_readings);
  //Scan_time = 1.5;
  Range_min = 0.0;
  Range_max = 100.00;
  Laser_msg.ranges_length = 180;
  Laser_msg.intensities_length = 180;
  Rservo.attach(Rservo_pin);
  initRanges();
  delay(1000);
}

float deg2Pi(float angle)
{
  float rad ;
  rad = angle /3.14159265 ;
  return rad;
}

float getDistance()
{  
   float randDistance;
   randDistance = random(0.5, 4.00);
   return randDistance;

}

void clearScan()
{
  for (int i = 0; i < 180; i=i+1) {
       Ranges[i]=0;
  }
}

void initRanges()
{
  for (int set_points = 0 ; set_points<180; set_points ++)
  {
    Ranges[set_points] = set_points;
    Intensities[set_points] = set_points*set_points;
  }
}

void loop() 
{
 if ((millis() - publisher_timer)> 50 ) 
  {
   
    Laser_msg.header.stamp = nh.now();
    Laser_msg.header.frame_id = "/Lidar_frame";
    Laser_msg.angle_min = Angle_min;
    Laser_msg.angle_max = Angle_max;
    Laser_msg.angle_increment = Angle_increment;
    Laser_msg.time_increment = Time_increment;
    Laser_msg.range_min = Range_min;
    Laser_msg.range_max = Range_max;                 

    // scan_time
    time_Later = millis();
    for (int angle_Setpoints = 0 ; angle_Setpoints < point_reading; angle_Setpoints ++)
    {
      delay(5);
     Rservo.write(angle_Setpoints);//(angle_Setpoints+1)*2); 
    // Serial.println((angle_Setpoints+1)*2); 
     Ranges[angle_Setpoints]= getDistance();
     Laser_msg.ranges[angle_Setpoints] =  Ranges[angle_Setpoints];
     Laser_msg.intensities[angle_Setpoints] =  Intensities[angle_Setpoints];
     
    }

    
    time_Now  = millis();
    Scan_time = time_Now - time_Later;
    Laser_msg.scan_time = Scan_time;
    pub_Laser.publish(&Laser_msg);
    publisher_timer = millis() ;
  }
  nh.spinOnce();
  delay(1000);

}
