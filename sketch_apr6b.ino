
// define global variables for analog pins.

// X values will be read from pin 0 and Y from pin 1

#define PIN_ANALOG_X 0
#define PIN_ANALOG_Y 1
#define BUTTON_UP 2
#define BUTTON_RIGHT 3
#define BUTTON_DOWN 4
#define BUTTON_LEFT 5
 
void setup() {
  Serial.begin(9600);
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

  int mappedX = map(xValue, 0, 968, -1, 1);
  int mappedY = map(yValue, 0, 1014, 1, -1);

  Serial.print(mappedX);
  Serial.print(",");
  Serial.print(mappedY);
  Serial.print(",");

  int up = digitalRead(BUTTON_UP);
  int right = digitalRead(BUTTON_RIGHT);
  int down = digitalRead(BUTTON_DOWN);
  int left = digitalRead(BUTTON_LEFT);
  Serial.print(up);
  Serial.print(",");
  Serial.print(right);
  Serial.print(",");
  Serial.print(down);
  Serial.print(",");
  Serial.println(left);

  delay(80); // Small delay for readability

}
