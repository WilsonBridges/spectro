#define SAMPLE_RATE 1000  // in Hz, adjust as needed
#define BUFFER_SIZE 64  // Number of samples per chunk

void setup() {
  Serial.begin(115200);
}

void loop() {
  for (int i = 0; i < BUFFER_SIZE; i++) {
    int piezoVal = analogRead(A0);  // Read piezo sensor data
    Serial.println(piezoVal);       // Send the reading over Serial
    delayMicroseconds(1000000 / SAMPLE_RATE);  // Sampling interval based on SAMPLE_RATE
  }
}