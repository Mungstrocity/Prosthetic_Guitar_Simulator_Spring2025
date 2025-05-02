import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=8)

while True:
    kit.continuous_servo[1].throttle = 1
    time.sleep(5)
    kit.continuous_servo[1].throttle = -1
    time.sleep(5)
