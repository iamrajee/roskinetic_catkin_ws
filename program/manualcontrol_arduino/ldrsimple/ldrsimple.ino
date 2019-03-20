void setup() {
  Serial.begin(57600);
}

void loop() {
  int sensorValue = analogRead(A0);
  Serial.println(sensorValue);
}
