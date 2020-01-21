/*
 * Main
 * Handles two buttons and sends a constant update signal over serial for 
*/

// constants won't change. They're used here to set pin numbers:
const int buttonPin1 = A0; // the number of the first pushbutton pin
const int buttonPin2 = A1; // the number of the second pushbutton pin
const int ledPin1 =  2;    // the number of the LED pin
const int ledPin2 =  3;    // the number of the LED pin
const int boardLed = 13;   // useful to record this

// variables will change:
int button1State = 0;      // variable for reading the first pressure sensor status
int button2State = 0;      // variable for reading the second pressure sensor status

void setup() {
  // initialize the LED pin as an output:
  pinMode(ledPin1, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  pinMode(boardLed, OUTPUT);
  
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin1, INPUT);
  pinMode(buttonPin2, INPUT);

  // initialize serial
  Serial.begin(9600);
}

void loop() {
  // read the state of the pushbutton value:
  button1State = analogRead(buttonPin1);
  button2State = analogRead(buttonPin2);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  // turn LED on:`
  digitalWrite(ledPin1, button1State > 100 ? HIGH : LOW);
  digitalWrite(ledPin2, button2State > 200 ? HIGH : LOW);

  Serial.print(button1State);
  Serial.print("&");
  Serial.print(button2State);
  Serial.print("|");
}
