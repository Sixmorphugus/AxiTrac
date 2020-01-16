/*
  Button

  Turns on and off a light emitting diode(LED) connected to digital pin 13,
  when pressing a pushbutton attached to pin 2.

  The circuit:
  - LED attached from pin 13 to ground
  - pushbutton attached to pin 2 from +5V
  - 10K resistor attached to pin 2 from ground

  - Note: on most Arduinos there is already an LED on the board
    attached to pin 13.

  created 2005
  by DojoDave <http://www.0j0.org>
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Button
*/

// constants won't change. They're used here to set pin numbers:
const int buttonPin = A0;     // the number of the pushbutton pin
const int ledPin1 =  2;      // the number of the LED pin
const int ledPin2 =  3;      // the number of the LED pin
const int ledPin3 =  4;      // the number of the LED pin
const int boardLed = 13;

// variables will change:
int buttonState = 0;         // variable for reading the pushbutton status

void setup() {
  // initialize the LED pin as an output:
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(ledPin3, OUTPUT);
  pinMode(boardLed, OUTPUT);
  
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);

  // initialize serial
  Serial.begin(9600);
}

void loop() {
  // read the state of the pushbutton value:
  buttonState = analogRead(buttonPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  // turn LED on:
  digitalWrite(boardLed, buttonState > 100 ? HIGH : LOW);
  digitalWrite(ledPin1, buttonState > 100 ? HIGH : LOW);
  digitalWrite(ledPin2, buttonState > 200 ? HIGH : LOW);
  digitalWrite(ledPin3, buttonState > 300 ? HIGH : LOW);

  Serial.print(buttonState);
  Serial.print("|");
}
