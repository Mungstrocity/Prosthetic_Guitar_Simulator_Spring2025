"""
Servo Motor Position Calibration

This script toggles between two preset positions for each servo to calibrate
and test specific positions for finger joints. It alternates between fully
extended and fully flexed positions for tip, middle, and abduction servos.

Parameters:
    - motors: Number of servo motors to control (default: 3)
    - min: Minimum angle in degrees (default: 0)
    - max: Maximum angle in degrees (default: 180)
    - delay: Delay between position toggles in seconds (default: 2)

Requirements:
    - adafruit_servokit library
    - Three servo motors connected to channels 0, 1, and 2:
      - Channel 0: Tip joint (extension/flexion)
      - Channel 1: Middle joint (flexion/extension)
      - Channel 2: Abduction joint

Usage:
    Run the script to start the position toggling.
    Press Ctrl+C to stop and reset all servos to zero position.

Position guide:
    - Position 1 (toggle=0):
      - Tip (index 0): 180° (extended)
      - Middle (index 1): 0° (flexed)
      - Abduction (index 2): 0° (neutral)
    
    - Position 2 (toggle=1):
      - Tip (index 0): 0° (flexed)
      - Middle (index 1): 180° (extended)
      - Abduction (index 2): 180° (abducted)
"""
from adafruit_servokit import ServoKit
import time

# Create a servo object
kit = ServoKit(channels=16)

motors = 3
angle = 0
min = 0
max = 180
increment = 25
maxscale = 2
delay = 2
toggle = 0
try:            
    while True:       
        if toggle == 0:
            kit.servo[0].angle = 180##Tip # up extend
            kit.servo[1].angle = 0#Middle # up flexes
            kit.servo[2].angle = 0##Abduction
            time.sleep(delay)
            toggle = 1
        else:
            kit.servo[0].angle = 0##Tip # up extend
            kit.servo[1].angle = 180#Middle # up flexes
            kit.servo[2].angle = 180##Abduction
            time.sleep(delay)
            toggle = 0
            
        
except KeyboardInterrupt:
    # Set all servo values to zero when exiting
    for i in range():
        kit.servo[i].angle = 0
    print("Servos set to zero")