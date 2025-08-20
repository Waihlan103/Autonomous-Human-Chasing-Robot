import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 115200)
time.sleep(2)  # Wait for Arduino to reset

while True:
    cmd = input("Enter Command (F/B/L/R/S): ")
    if cmd in ['F', 'B', 'L', 'R', 'S']:
        ser.write(cmd.encode())  # Send single character
        print(f"Sent: {cmd}")
    else:
        print("Invalid command")
