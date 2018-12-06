class HardwareStub{
  /*Hardware Stub for ADXL345
    Test Case: Expected outputs when ADXL345 is in a steady state 
    (10 values)
  */
  public:
  virtual void analogReadSteady() {
    Serial.println("230");
    Serial.println("253");
    Serial.println("232");
    Serial.println("257");
    Serial.println("195");
    Serial.println("201");
    Serial.println("210");
    Serial.println("244");
    Serial.println("297");
    Serial.println("330");
  }
  /*Hardware Stub for ADXL345
    Test Case: Expected outputs when ADXL345 in a turning phase
    (10 values)
  */
  virtual void analogReadTurning() {
    Serial.println("550");
    Serial.println("570");
    Serial.println("803");
    Serial.println("590");
    Serial.println("693");
    Serial.println("992");
    Serial.println("1003");
    Serial.println("884");
    Serial.println("750");
    Serial.println("744");
  }
  	
  
  /*Hardware Stub for ADXL345
    Test Case: Expected outputs when ADXL345 is completing a turn
    (10 values)
  */
  virtual void analogReadTurned() {
    Serial.println("180");
    Serial.println("179");
    Serial.println("190");
    Serial.println("178");
    Serial.println("163");
    Serial.println("185");
    Serial.println("174");
    Serial.println("173");
    Serial.println("185");
    Serial.println("189");
  }
};

const int BAUD_RATE = 9600;
HardwareStub *hs;
boolean done = false;

void setup(){
  Serial.begin(BAUD_RATE);
  hs = new HardwareStub();
}

void loop(){
  
    hs->analogReadSteady();
    delay(2000);
    hs->analogReadTurning();
    delay(2000);
    hs->analogReadTurned();
    delay(2000);
   
     //do nothing
   }
