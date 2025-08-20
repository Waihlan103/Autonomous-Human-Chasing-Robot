#include <PID_control.hpp>

float LKp = 2.2, LKi = 0.5, LKd = 0.003;
float RKp = 2.45, RKi = 0.5, RKd = 0.003;
float previousErrorLeft = 0.0, previousErrorRight = 0.0;
float integralLeft = 0.0, integralRight = 0.0;
unsigned long lastTime = 0;
const int PPR = 890; // Pulses per revolution of the motor
int motorSpeedLeft = 0, motorSpeedRight = 0;

void PID_control() {
    unsigned long currentTime = millis();
    //float dt = (currentTime - lastTime) / 1000;
    if (currentTime - lastTime >= 50) { // Every 100ms
        // Convert encoder counts to RPM
        //float leftRPM = (leftCount / (float)PPR) * (60 / dt);
        //float rightRPM = (rightCount / (float)PPR) * (60 / dt);
        float leftRPM = (leftCount / (float)PPR) * 1200;
        float rightRPM = (rightCount / (float)PPR) * 1200;
        
        leftRPM = abs(leftRPM);
        rightRPM = abs(rightRPM);

        // Calculate errors
        float errorLeft = LtargetRPM - leftRPM;
        float errorRight = RtargetRPM - rightRPM;

        // Proportional term
        float P_termLeft = LKp * errorLeft;
        float P_termRight = RKp * errorRight;

        // Integral term
        //integralLeft += errorLeft * dt;
        //integralRight += errorRight * dt;
        integralLeft += errorLeft;
        integralRight += errorRight;
        float I_termLeft = LKi * integralLeft;
        float I_termRight = RKi * integralRight;

        // Derivative term
        //float D_termLeft = LKd * ((errorLeft - previousErrorLeft) / dt);
        //float D_termRight = RKd * ((errorRight - previousErrorRight) / dt);
        float D_termLeft = LKd * (errorLeft - previousErrorLeft);
        float D_termRight = RKd * (errorRight - previousErrorRight);

        // PID output
        motorSpeedLeft = constrain(P_termLeft + I_termLeft + D_termLeft, 0, 255);
        motorSpeedRight = constrain(P_termRight + I_termRight + D_termRight, 0, 255);

        // Send motor speeds to the motor driver
        motor.move(direction, motorSpeedLeft, motorSpeedRight);

        // Update previous errors
        previousErrorLeft = errorLeft;
        previousErrorRight = errorRight;
        leftCount = 0;
        rightCount = 0;

        lastTime = currentTime;
    }
}
