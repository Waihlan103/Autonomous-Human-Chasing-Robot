#ifndef ENCODER_HPP
#define ENCODER_HPP
#include <Arduino.h>

#define ENC_LEFT_A 35
#define ENC_LEFT_B 34
#define ENC_RIGHT_A 16
#define ENC_RIGHT_B 17

extern volatile int leftCount;
extern volatile int rightCount;

void IRAM_ATTR leftISR();
void IRAM_ATTR rightISR();
void encoder_init();
#endif