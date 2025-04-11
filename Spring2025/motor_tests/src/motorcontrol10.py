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