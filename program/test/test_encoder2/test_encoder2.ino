//#include<math.h>
// ===================================== VARIABLES =======================================
//int BA = 42;
//int BB = 43;
//int m1=50;
//int m2=51;
//int enpin = 4;

int BA = 44;
int BB = 45;
int m1=52;
int m2=53;
int enpin = 5;

long enPos = 0;
int BA_prev = LOW;
int n = LOW;
int Hspeed = 255;
int Lspeed = 120;
//======================================================================================
int enval = 1;
int Speed = 130;//130; //IN RANGE (75,255)
int SPFC = 100;//130;
int SPBC = 100;//130;
// ===================================== SETUP =======================================

void setup() {
  pinMode (BA, INPUT);
  pinMode (BB, INPUT);
  pinMode (m1, OUTPUT);
  pinMode (m2, OUTPUT);
  pinMode (enpin, OUTPUT);
  digitalWrite(enpin, enval);
  Serial.begin (9600);
}

//======================================= FUNCTIONS ==========================================
void encoder(){
//  Serial.print(digitalRead(BA));
//  Serial.print(",");
//  Serial.println(digitalRead(BB));
  n = digitalRead(BA);
  if ((BA_prev == LOW) && (n == HIGH)) {
    if (digitalRead(BB) == LOW) {
      enPos++;
    } else {
      enPos--;
    }
    Serial.println(enPos);
    //Serial.print ("/");
    //Serial.println (Speed);
  }
  BA_prev = n;
}

void f(){
  analogWrite(m1, Speed);
  digitalWrite(m2, 0); 
}
void b(){
  digitalWrite(m1, 0);
  analogWrite(m2, Speed); 
}
void s(int d){
  enPos = 0;
  digitalWrite(m1, 0);
  digitalWrite(m2, 0);
  delay(d);
}
void fstep(int nstep){
  int t = enPos;
  f();
//  abs(enPos-t)
  while(enPos-t<nstep){
    //f();
   //Speed=map(enPos-t,0,nstep+1,Hspeed,Lspeed);
   encoder();
  }
  s(0);
}
void bstep(int nstep){
  int t = enPos;
  b(); 
//  abs(t-enPos)
  while(abs(t-enPos)<nstep){
    //b();
    //Speed=map(t-enPos,0,nstep,Hspeed,Lspeed);
    encoder();
  }
  s(0);
}
//======================================== LOOP =========================================
void loop() {
  fstep(1*SPFC);
  s(3000);
  bstep(1*SPBC);
  s(3000);
//  b();
//  encoder();
}
