#include <encoder.hpp>

volatile int leftCount = 0;
volatile int rightCount = 0;

void encoder_init(){
  pinMode(ENC_LEFT_A, INPUT_PULLUP);
  pinMode(ENC_LEFT_B, INPUT_PULLUP);
  pinMode(ENC_RIGHT_A, INPUT_PULLUP);
  pinMode(ENC_RIGHT_B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(ENC_LEFT_A), leftISR, RISING);
  attachInterrupt(digitalPinToInterrupt(ENC_RIGHT_A), rightISR, RISING);
}
void IRAM_ATTR leftISR() {
  if (digitalRead(ENC_LEFT_B) == HIGH) leftCount++;  // Check B signal for direction
  else leftCount--;
}

void IRAM_ATTR rightISR() {
  if (digitalRead(ENC_RIGHT_B) == HIGH) rightCount++; // Check B signal for direction
  else rightCount--;
}