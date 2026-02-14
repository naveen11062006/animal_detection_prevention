const int ledPin = 12;
const int buzzerPin = 10;

char receivedData = '0';

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {

  if (Serial.available()) {
    receivedData = Serial.read();
  }

  if (receivedData == '1') {
    blinkLED();
    tone(buzzerPin, 500);   // Low sound
  }
  else if (receivedData == '2') {
    blinkLED();
    tone(buzzerPin, 1000);  // Medium sound
  }
  else if (receivedData == '3') {
    blinkLED();
    tone(buzzerPin, 2000);  // High sound
  }
  else {
    digitalWrite(ledPin, LOW);
    noTone(buzzerPin);
  }
}

void blinkLED() {
  digitalWrite(ledPin, HIGH);
  delay(200);
  digitalWrite(ledPin, LOW);
  delay(200);
}
