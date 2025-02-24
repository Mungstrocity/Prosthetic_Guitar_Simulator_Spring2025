from adafruit_servokit import ServoKit
import time

# Create a servo object
kit = ServoKit(channels=16)

angle = 0
min = 0
max = 180
increment = max
maxscale = 2
delay = 1

try:
    while True:
        while angle < max:
            kit.servo[0].angle = angle
            kit.servo[1].angle = angle
            kit.servo[2].angle = angle
            kit.servo[3].angle = angle
            time.sleep(delay)
            if angle + increment >= 180:
                angle = 180
                time.sleep(maxscale * delay)
            else:
                angle += increment
            print(angle)
            
        while angle > 0.0:
            kit.servo[0].angle = angle
            kit.servo[1].angle = angle
            kit.servo[2].angle = angle
            kit.servo[3].angle = angle
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