#include <serial_communication.hpp>

uint8_t direction;

int LtargetRPM = 0; // Desired RPM
int RtargetRPM = 0; // Desired RPM
int LSpeed = 0;
int RSpeed = 0;

serialcommunication syscom;
MotorControl motor;

serialcommunication::serialcommunication()
{
}

void serialcommunication::operation(){
    while(Serial.available() > 0) {  // Check if data is available to read
        _serial_read = Serial.read();     // Read the incoming byte
    
        // Print the received command for confirmation
        Serial.print("Received Command: ");
        Serial.println(_serial_read);
    
        // Act based on the command
        switch (_serial_read) {
          case 'F':
            moveForward();
            break;
          case 'B':
            moveBackward();
            break;
          case 'R':
            turnRight();
            break;
          case 'L':
            turnLeft();
            break;
          case 'S':
            stopMoving();
            break;
          
          default:
            Serial.read();
            Serial.println("invalid");
            break;
        }
        LtargetRPM = LSpeed;
        RtargetRPM = RSpeed;
      }
}

void serialcommunication::moveForward()
{
    direction = FORWARD;
    LSpeed = 8;
    RSpeed = 8;
}
void serialcommunication::moveBackward()
{
    direction = BACKWARD;
    LSpeed = 8;
    RSpeed = 8;
}
void serialcommunication::turnLeft()
{
    direction = LEFT;
    LSpeed = 8;
    RSpeed = 8;
}
void serialcommunication::turnRight()
{
    direction = RIGHT;
    LSpeed = 8;
    RSpeed = 8;
}

void serialcommunication::stopMoving(){
    direction = STOP;
    LSpeed = 0;
    RSpeed = 0;
}

serialcommunication::~serialcommunication()
{
}