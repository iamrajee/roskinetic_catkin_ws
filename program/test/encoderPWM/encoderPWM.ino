// ===================================== VARIABLES =======================================
int encoder0PinA = 42;
int encoder0PinB = 43;
int m1=50;
int m2=51;
int enpin = 4;

long encoder0Pos = 0;
int encoder0PinALast = LOW;
int n = LOW;
//======================================================================================
//                                                                                      |
//                            MODIFY PARAMETERS  HERE                                   |
//                                                                                      |
//======================================================================================
int enval = 1;
int Speed = 255; //IN RANGE (75,255)
int SPFC = 190;
int SPBC = 160;
// ===================================== SETUP =======================================

void setup() {
  pinMode (encoder0PinA, INPUT);
  pinMode (encoder0PinB, INPUT);
  pinMode (m1, OUTPUT);
  pinMode (m2, OUTPUT);
  pinMode (enpin, OUTPUT);
  digitalWrite(enpin, enval);
  Serial.begin (9600);
}

//======================================= FUNCTIONS ==========================================
void encoder(){
  n = digitalRead(encoder0PinA);
  if ((encoder0PinALast == LOW) && (n == HIGH)) {
    if (digitalRead(encoder0PinB) == LOW) {
      encoder0Pos--;
    } else {
      encoder0Pos++;
    }
    Serial.println(encoder0Pos);
    //Serial.print ("/");
    //Serial.println (Speed);
  }
  encoder0PinALast = n;
}

void b(){
  analogWrite(m1, Speed);
  digitalWrite(m2, 0); 
}
void f(){
  digitalWrite(m1, 0);
  analogWrite(m2, Speed); 
}
void s(int d){
  //encoder0Pos = 0;
  digitalWrite(m1, 0);
  digitalWrite(m2, 0);
  delay(d);
}
void fstep(int nstep){
  int t = encoder0Pos;
  
  while(encoder0Pos-t<nstep){
    f();
   Speed=map(encoder0Pos-t,0,nstep+1,255,75);
   encoder();
  }
}
void bstep(int nstep){
  int t = encoder0Pos;
  
  while(t-encoder0Pos<nstep){
    b();
    Speed=map(t-encoder0Pos,0,nstep+1,255,75);
    encoder();
  }
}
//======================================== LOOP =========================================
void loop() {
  fstep(2*SPFC);
  s(3000);
  bstep(2*SPBC);
  s(3000);
    //b();
}
