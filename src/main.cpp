#include <Arduino.h>
#include <encoder.hpp>
#include <motor_control.hpp>
#include <serial_communication.hpp>
#include <PID_control.hpp>

void setup() {
    Serial.begin(115200);
    encoder_init();
}

void loop() {
    syscom.operation();
    PID_control();
}
