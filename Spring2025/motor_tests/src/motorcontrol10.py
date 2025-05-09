"""
Servo Motor Sweep Control

This script controls multiple servo motors by sweeping them between minimum and 
maximum angle positions in synchronization. All servos move to the same angle 
simultaneously, with configurable speed and range parameters.

Parameters:
    - motors: Number of servo motors to control (default: 3)
    - min: Minimum angle in degrees (default: 0)
    - max: Maximum angle in degrees (default: 80)
    - increment: Angle change per step in degrees (default: 5)
    - maxscale: Multiplier for delay time at extremes (default: 2)
    - delay: Base delay between angle changes in seconds (default: 1)

Requirements:
    - adafruit_servokit library
    - Servo motors connected to channels 0, 1, 2 on a servo controller

Usage:
    Run the script to start the servo sweep.
    Press Ctrl+C to stop and reset all servos to zero position.
"""
from adafruit_servokit import ServoKit
import time

# Create a servo object
kit = ServoKit(channels=16)

motors = 3
angle = 0
min = 0
max = 80
increment = 5
maxscale = 2
delay = 1

try:
    while True:
        while angle < max:
            for i in range(motors):
                kit.servo[i].angle = angle
            time.sleep(delay)
            if angle + increment >= max:
                angle = max
                time.sleep(maxscale * delay)
            else:
                angle += increment
            print(angle)
            
        while angle > 0.0:
            for i in range(motors):
                kit.servo[i].angle = angle
            time.sleep(delay)
            if angle - increment <= 0:
                angle = 0
                time.sleep(maxscale * delay)
            else:
                angle -= increment
            print(angle)
except KeyboardInterrupt:
    # Set all servo values to zero when exiting
    for i in range(4):
        kit.servo[i].angle = 0
    print("Servos set to zero")