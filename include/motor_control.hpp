#ifndef MOTOR_CONTROL_HPP
#define MOTOR_CONTROL_HPP

#include <Arduino.h>
// ==== Motor A Pins ====
#define MOTOR_A_IN1 12
#define MOTOR_A_IN2 14

// ==== Motor B Pins ====
#define MOTOR_B_IN1 26
#define MOTOR_B_IN2 27

#define FORWARD 0x06
#define BACKWARD 0x09
#define LEFT 0x05
#define RIGHT 0x0A       
#define STOP 0x00

class MotorControl{
     private:

     public:
          MotorControl();
          void move(uint8_t direction, uint8_t left_speed, uint8_t right_speed);
          ~MotorControl();
};

#endif