int triggerpin = 40;
int echopin = 41;
int distance, t;

void setup(){
  Serial.begin(57600);
  pinMode(triggerpin, OUTPUT); //TO ULTRA SONIC SENSOR
  pinMode(echopin, INPUT);   //FORM ULTRA SONIC SENSOR
}

void loop(){
  digitalWrite(triggerpin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerpin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerpin, LOW);
  
  
  digitalRead(echopin);
  
  t = pulseIn(echopin, HIGH);
  
  distance = t*(0.034)/2;
  Serial.println(distance);
}
