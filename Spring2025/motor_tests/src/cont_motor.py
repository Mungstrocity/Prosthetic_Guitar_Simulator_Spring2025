"""
Continuous Servo Motor Test

This script tests a continuous rotation servo motor by alternating between
forward and reverse rotation. The motor will run at full speed forward for
5 seconds, then full speed reverse for 5 seconds, in an infinite loop.

Requirements:
    - adafruit_servokit library
    - A continuous rotation servo connected to channel 1 on the servo controller

Usage:
    Run this script to start the motor test.
    Press Ctrl+C to stop the test.
"""
import time
from adafruit_servokit import ServoKit

# Initialize the servo controller with 8 channels
kit = ServoKit(channels=8)

while True:
    # Set the continuous servo on channel 1 to full forward speed
    kit.continuous_servo[1].throttle = 1
    time.sleep(5)
    # Set the continuous servo on channel 1 to full reverse speed
    kit.continuous_servo[1].throttle = -1
    time.sleep(5)
