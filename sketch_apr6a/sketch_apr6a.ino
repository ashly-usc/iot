// define global variables for analog pins.

// X values will be read from pin 0 and Y from pin 1

#define PIN_ANALOG_X 0
#define PIN_ANALOG_Y 1
#define BUTTON_UP 2
#define BUTTON_RIGHT 3
#define BUTTON_DOWN 4
#define BUTTON_LEFT 5



#define DELAY 500
 

void setup() {

 // Start serial because we will observe values at serial monitor

 Serial.begin(9600);



 // to enable pull up resistors first write pin mode

 // and then make that pin HIGH

 pinMode(BUTTON_UP, INPUT);

 digitalWrite(BUTTON_UP, HIGH);



 pinMode(BUTTON_RIGHT, INPUT);

 digitalWrite(BUTTON_RIGHT, HIGH);



 pinMode(BUTTON_DOWN, INPUT);

 digitalWrite(BUTTON_DOWN, HIGH);



 pinMode(BUTTON_LEFT, INPUT);

 digitalWrite(BUTTON_LEFT, HIGH);





}

 

void loop() {
  int xValue = analogRead(PIN_ANALOG_X);
  int yValue = analogRead(PIN_ANALOG_Y);


  // Serial.print("X: ");
  // Serial.print(xValue);
  // Serial.print(" | Y: ");
  // Serial.print(yValue);
  // Serial.println();

  int hi = digitalRead(BUTTON_UP);
  Serial.println(hi);

if(digitalRead(BUTTON_UP) == LOW) {

   Serial.println("Button A is pressed");

   delay(DELAY);

 }

//  else if(digitalRead(BUTTON_RIGHT) == LOW) {

//    Serial.println("Button B is pressed");

//    delay(DELAY);

//  }

//  else if(digitalRead(BUTTON_DOWN) == LOW) {

//    Serial.println("Button C is pressed");

//    delay(DELAY);

//  }

//  else if(digitalRead(BUTTON_LEFT) == LOW) {

//    Serial.println("Button D is pressed");

//    delay(DELAY);

//  }

//  else if(digitalRead(BUTTON_E) == LOW) {

//    Serial.println("Button E is pressed");

//    delay(DELAY);

//  }

//  else if(digitalRead(BUTTON_F) == LOW) {

//    Serial.println("Button F is pressed");

//    delay(DELAY);

//  }

  delay(100); // Small delay for readability

}
