#include <Arduino.h>
#include <motor_control.hpp>
#include <serial_communication.hpp>

MotorControl::MotorControl(){
     // Motor pins
     pinMode(MOTOR_A_IN1, OUTPUT);
     pinMode(MOTOR_A_IN2, OUTPUT);
     pinMode(MOTOR_B_IN1, OUTPUT);
     pinMode(MOTOR_B_IN2, OUTPUT);
} 

void MotorControl::move(uint8_t direction, uint8_t left_speed, uint8_t right_speed){
     analogWrite(MOTOR_A_IN1, left_speed * (direction & 0x01) >> 0);
     analogWrite(MOTOR_A_IN2, left_speed * (direction & 0x02) >> 1);
     analogWrite(MOTOR_B_IN1, right_speed * (direction & 0x04) >> 2);
     analogWrite(MOTOR_B_IN2, right_speed * (direction & 0x08) >> 3);
     return;
}

MotorControl::~MotorControl(){
}