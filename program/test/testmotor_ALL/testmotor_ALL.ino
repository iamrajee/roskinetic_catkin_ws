//#include <ArduinoHardware.h>
#define Flm_en 2
#define Frm_en 3
#define Flm1   46
#define Flm2   47
#define Frm1   48
#define Frm2   49

#define Blm_en 4
#define Brm_en 5
#define Blm1   50
#define Blm2   51
#define Brm1   52
#define Brm2   53

//int lowSpeed = 100;
//int highSpeed = 255;
int Speed = 100;
int FSpeed = 100;
int BSpeed = 120;
int FlSpeed = FSpeed;
int FrSpeed = FSpeed;
int BlSpeed = BSpeed;
int BrSpeed = BSpeed;

void setup()
{
//**********FRONT MOTOR **********//
  pinMode(Flm1, OUTPUT);
  pinMode(Flm2, OUTPUT);
  pinMode(Flm_en, OUTPUT);
  pinMode(Frm1, OUTPUT);
  pinMode(Frm2, OUTPUT);
  pinMode(Frm_en, OUTPUT);
  //initialization of motors
  digitalWrite(Flm1, 0);
  digitalWrite(Flm2, 0);
  digitalWrite(Frm1, 0);
  digitalWrite(Frm2, 0);
  analogWrite(Flm_en, 0);
  analogWrite(Frm_en, 0);
//**********BACK MOTOR **********//
  pinMode(Blm1, OUTPUT);
  pinMode(Blm2, OUTPUT);
  pinMode(Blm_en, OUTPUT);
  pinMode(Brm1, OUTPUT);
  pinMode(Brm2, OUTPUT);
  pinMode(Brm_en, OUTPUT);
  //initialization of motors
  digitalWrite(Blm1, 0);
  digitalWrite(Blm2, 0);
  digitalWrite(Brm1, 0);
  digitalWrite(Brm2, 0);
  analogWrite(Blm_en, 0);
  analogWrite(Brm_en, 0); 
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
  digitalWrite(Flm1, lm1_v);
  digitalWrite(Flm2, lm2_v);
  digitalWrite(Frm1, rm1_v);
  digitalWrite(Frm2, rm2_v);
  analogWrite(Flm_en, FlSpeed);
  analogWrite(Frm_en, FrSpeed);

  digitalWrite(Blm1, lm1_v);
  digitalWrite(Blm2, lm2_v);
  digitalWrite(Brm1, rm1_v);
  digitalWrite(Brm2, rm2_v);
  analogWrite(Blm_en, BlSpeed);
  analogWrite(Brm_en, BrSpeed);
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
  analogWrite(Flm_en, 0);
  analogWrite(Frm_en, 0);
  analogWrite(Blm_en, 0);
  analogWrite(Brm_en, 0);
}
