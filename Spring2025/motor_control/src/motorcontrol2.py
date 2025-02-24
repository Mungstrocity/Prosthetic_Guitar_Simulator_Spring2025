from adafruit_servokit import ServoKit
import time

# Create a servo object
kit = ServoKit(channels=16)

angle = 0
min = 0
max = 180
throttle = 1
thr_coeff = 2
increment = 2
delay = 0.001
while True:
    while angle < max:
        kit.servo[0].angle = angle
        kit.servo[1].angle = angle
        time.sleep(delay)
        if angle + increment >= 180:
            angle = 180
            time.sleep(5 * delay)
        else:
            angle += increment
        print(angle)
        
    while angle > 0.0:
        kit.servo[0].angle = angle
        kit.servo[1].angle = angle
        time.sleep(delay)
        if angle - increment <= 0:
            angle = 0
            time.sleep(5 * delay)
        else:
            angle -= increment
        print(angle)
    
    

