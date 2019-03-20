#include <ros.h>
#include <std_msgs/Float64.h>

ros::NodeHandle nh;
std_msgs::Float64 Distance;
ros::Publisher ultrasonicpub("ultrasonic",&Distance);

// defines pins numbers
const int trigPin = 26;
const int echoPin = 27;

// defines variables
long duration;
float distance;

void setup() {
  nh.initNode();
  nh.advertise(ultrasonicpub);
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin(57600); // Starts the serial communication
}

void loop() {
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);//in micro second
  distance= duration*0.034/2;
  Distance.data=distance;
  ultrasonicpub.publish(&Distance);
  nh.spinOnce();
  // Prints the distance on the Serial Monitor
  //Serial.print("Distance: ");
  //Serial.println(distance);
  //delay(100);
}
