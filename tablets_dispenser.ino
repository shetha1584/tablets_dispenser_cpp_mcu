int slot_0=12,slot_1=11,slot_2=10;
String inputString = "";         // a String to hold incoming data
bool stringComplete = false;  // whether the string is complete
long int t1, t2;
// the setup function runs once when you press reset or power the board
#include <Servo.h>


Servo myservo; 
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(slot_0, INPUT);
  pinMode(slot_1, INPUT);
  pinMode(slot_2, INPUT);
  Serial.begin(9600);
  inputString.reserve(200);
   myservo.attach(9);
}

int check_tablets(int slot){
  if(digitalRead(slot)==0){
      return 0;
    }
    return 1;
  }


 void warning_slot(int slot){
  if(check_tablets(slot)==0){
    
    while(check_tablets(slot)==0){
      t2 = millis();
      if(t2>(t1+10000)){
        digitalWrite(LED_BUILTIN, HIGH);
      }
      }
    delay(10);
    }
    t2=0;
  }
// the loop function runs over and over again forever
void loop() {
  serialEvent();
  
  t1 = millis();
  //warning_slot(slot_0);
  // warning_slot(slot_1);
  // warning_slot(slot_2);
  digitalWrite(LED_BUILTIN, LOW);
    
 if (stringComplete) {
    Serial.println(inputString);
    // clear the string:
    Serial.println(sizeof(inputString));
    if(inputString=="data\r\n"){
    
      myservo.write(180);
      delay(15);
      
      }
    inputString = "";
    stringComplete = false;
  }
  myservo.write(0);
  
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
