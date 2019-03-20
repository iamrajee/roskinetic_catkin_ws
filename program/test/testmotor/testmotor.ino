//#include <ArduinoHardware.h>
#define lm_en 2
#define rm_en 3
#define lm1   46
#define lm2   47
#define rm1   48
#define rm2   49

//#define lm_en 4
//#define rm_en 5
//#define lm1   50
//#define lm2   51
//#define rm1   52
//#define rm2   53

//int lowSpeed = 220;
//int highSpeed = 30;
int Speed = 100;
int lSpeed = Speed;
int rSpeed = Speed;

void setup()
{
  pinMode(lm1, OUTPUT);
  pinMode(lm2, OUTPUT);
  pinMode(lm_en, OUTPUT);
  pinMode(rm1, OUTPUT);
  pinMode(rm2, OUTPUT);
  pinMode(rm_en, OUTPUT);

 //initialization of motors
  digitalWrite(lm1, 0);
  digitalWrite(lm2, 0);
  digitalWrite(rm1, 0);
  digitalWrite(rm2, 0);
  
  analogWrite(lm_en, 0);
  analogWrite(rm_en, 0); 
} 

void loop()
{
  //sleft();
  //left();
  //sright();
  //right();
  forward();
  //backward();
  delay(1000);
}
void setmotor(int lm1_v,int lm2_v,int rm1_v, int rm2_v){
  digitalWrite(lm1, lm1_v);
  digitalWrite(lm2, lm2_v);
  digitalWrite(rm1, rm1_v);
  digitalWrite(rm2, rm2_v);
  analogWrite(lm_en, lSpeed);
  analogWrite(rm_en, rSpeed);
}
void forward(){
  setmotor(1,0,1,0);
}
void backward(){
  setmotor(0,1,0,1);
}
void left(){
  setmotor(0,1,1,0);
}
void right(){
  setmotor(1,0,0,1); 
}
void sleft(){
  setmotor(0,0,1,0);
}
void sright(){
  setmotor(1,0,0,0);
}
void Stop(){
  setmotor(0,0,0,0);
  analogWrite(lm_en, 0);
  analogWrite(rm_en, 0);
}
