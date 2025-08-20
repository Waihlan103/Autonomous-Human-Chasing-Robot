#ifndef SERIAL_COMMUNICATION_HPP
#define SERIAL_COMMUNICATION_HPP

#include <motor_control.hpp>
#include <encoder.hpp>
#include <Arduino.h>
#include <PID_control.hpp>

extern uint8_t direction;

extern int LtargetRPM; // Desired RPM
extern int RtargetRPM; // Desired RPM
extern MotorControl motor;
extern int LSpeed;
extern int RSpeed;

class serialcommunication
{
private:
    char _serial_read = '\n';
    //int speed_ = 0;

public:
    serialcommunication();
    void operation();
    void moveForward();
    void moveBackward();
    void turnLeft();
    void turnRight();
    void stopMoving();
    ~serialcommunication();
};
extern serialcommunication syscom;

#endif