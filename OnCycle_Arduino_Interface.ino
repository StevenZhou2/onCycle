/*
OnCycle Project - Hardware Interface
-----------------------------------------
Project: SYSC 3010 - OnCycle Project
Author: Christian Sargusingh
Date: 2018-11-20
-----------------------------------------
Description: This file contains the hardware code for the 
turning signals, brake light interfacing using DPST push 
switches. This code is also responsible for reading
accelerometer data from the ADXL345.
*/

const int DELAY = 400;
const byte LEFT_PIN = 3;
const byte RIGHT_PIN = 5;
const byte BRAKE_PIN = 4;

const byte LEFT_IN = 11;
const byte RIGHT_IN = 13;
const byte BRAKE_IN = 12;

const byte xpin = A3;
const byte ypin = A2;

const byte zpin = A1;
const byte gndpin = 18;
const byte pwrpin = 19;

//State variables for blink control
boolean leftState = 0;
boolean rightState = 0;
boolean brakeState = 0;

boolean blState = 1;
boolean brState = 1;


//timing variables and debouncing constants
const int PULSE_TIME = 10000;
const int DB_TIME = 250;
int t1 = 0;
int timer = 0;

//accelerometer variable
int analog = 0;
String packet;
void setup(){
  //Define serial communications (9600 baud)
  Serial.begin(9600);
  
  //initialize digital i/o pin 13 and 12 as input (btn pins)
  pinMode(LEFT_IN,INPUT);  //left
  pinMode(RIGHT_IN,INPUT);  //right
  pinMode(BRAKE_IN,INPUT);
  
  //initialize digital i/o(LED pins)
  pinMode(BRAKE_PIN,OUTPUT);  //brake
  pinMode(LEFT_PIN,OUTPUT);  //left
  pinMode(RIGHT_PIN,OUTPUT);  //right
  pinMode(gndpin,OUTPUT);
  pinMode(pwrpin, OUTPUT);
  pinMode(BRAKE_PIN,OUTPUT);  //brake
  pinMode(LEFT_PIN,OUTPUT);  //left
  pinMode(RIGHT_PIN,OUTPUT);  //right
  pinMode(gndpin,OUTPUT);
  
  //Write 1 and 0 to accelerometer
  digitalWrite(gndpin, LOW);
  digitalWrite(pwrpin, HIGH);
}

/* MAIN EVENT LOOP*/
void loop(){
  //increment timer counter
  timer = timer+1;
  
  /*BRAKE LIGHT IMPLEMENTATION
    ------------------------------------------------------- */
  //always write 0 unless brake btn is pressed down
  digitalWrite(BRAKE_PIN,LOW);
  brakeState = 0;
  //if brake btn is pushed write high to the brake pin until the btn is released
  if (digitalRead(BRAKE_IN) == 0){
    digitalWrite(BRAKE_PIN,HIGH);
    brakeState = 1;
  }
  
  /*LEFT SIGNAL IMPLEMENTATION
  ------------------------------------------------------- */
  if (digitalRead(LEFT_IN) == 0){
    if (leftState){
      digitalWrite(LEFT_PIN,LOW);
      leftState = 0;
      timer = 0;
    }else{
      leftState = 1;
      digitalWrite(RIGHT_PIN,LOW);
      rightState = 0;
    }
    //send left button state to db
    delay(DB_TIME);
  }
  
  if ((leftState)&&(timer == PULSE_TIME)){
    blState = !blState;
    if (blState){
      digitalWrite(LEFT_PIN,HIGH);
    }else{
      digitalWrite(LEFT_PIN,LOW);
    }
    //reset timer for next cycle
    timer = 0;
  }
  
  
  /*RIGHT SIGNAL IMPLEMENTATION
  ------------------------------------------------------- */
  if (digitalRead(RIGHT_IN) == 0){
    if (rightState){
      digitalWrite(RIGHT_PIN,LOW);
      rightState = 0;
      timer = 0;
    }else{
      rightState = 1;
      digitalWrite(LEFT_PIN,LOW);
      leftState = 0;
    }
    //send right button state to db
    delay(DB_TIME);
  }
  
  if ((rightState)&&(timer == PULSE_TIME)){
    brState = !brState;
    if (brState){
      digitalWrite(RIGHT_PIN,HIGH);
    }else{
      digitalWrite(RIGHT_PIN,LOW);
    }
    //reset timer for next cycle
    timer = 0;
  }
    
  if (timer%1000 == 0){
    analog = analogRead(zpin);
    Serial.print(leftState);
    Serial.print(brakeState);
    Serial.print(rightState);
    Serial.println(analog);
    
    if (analog > 550){
      rightState = false;
      digitalWrite(RIGHT_PIN, LOW);
      leftState = false;
      digitalWrite(LEFT_PIN, LOW);
    }
  }
}


