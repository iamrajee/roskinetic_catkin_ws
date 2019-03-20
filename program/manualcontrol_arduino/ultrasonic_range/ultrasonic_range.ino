#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

//************** INCLUDE ****************//
#include <ros.h>
#include <ros/time.h>
#include <sensor_msgs/Range.h>

//*************** PIN ****************//
const int trigPin = 26;
const int echoPin = 27;

//*************** NODE ****************//
ros::NodeHandle nh;

//*************** Publisher ****************//
sensor_msgs::Range range_msg;
ros::Publisher ultrasonicpub("ultrasonicRange",&range_msg);

//*************** variables ****************//
long duration;
float distance;
long ultra_pub_time;

//*************** MAIN SETUP ***************//
void setup() {
  nh.initNode();
  ultra_setup();
}
//*************** MAIN LOOP ***************//
void loop(){
  nh.spinOnce();
  ultra_loop();
}
//*************** ULTRA SETUP *************//
void ultra_setup() {
  nh.advertise(ultrasonicpub);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  range_msg.radiation_type = sensor_msgs::Range::ULTRASOUND;
  range_msg.header.frame_id =  "/ultrasound";
  range_msg.field_of_view = 0.1;  // fake
  range_msg.min_range = 0.0;
  range_msg.max_range = 3310.0;
  ultra_pub_time =  millis();
}
//*************** ULTRA LOOP *************//
void ultra_loop() {
  if ( millis() - ultra_pub_time >=50){
    range_msg.range = get_ultraDist();
    range_msg.header.stamp = nh.now();
    ultrasonicpub.publish(&range_msg);
    ultra_pub_time =  millis();
  }
}
//*************** ULTRA DIST *************//
float get_ultraDist() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);//in micro second
  distance= duration*0.034/2;
  return distance;
}
