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
#     while True:
#         while angle < max:
#             for i in range(motors):
#                 kit.servo[i].angle = angle
#             time.sleep(delay)
#             if angle + increment >= max:
#                 angle = max
#                 time.sleep(maxscale * delay)
#             else:
#                 angle += increment
#             print(angle)
            
#         while angle > 0.0:
#             for i in range(motors):
#                 kit.servo[i].angle = angle
#             time.sleep(delay)
#             if angle - increment <= 0:
#                 angle = 0
#                 time.sleep(maxscale * delay)
#             else:
#                 angle -= increment
#             print(angle)
            
    while True:       
        ## Increasing is 
        # kit.servo[0].angle = 180##Tip # up extend
        # kit.servo[1].angle = 0#Middle # up flexes
        # kit.servo[2].angle = 0##Abduction
        # # time.sleep(delay)
        #toggle = 1
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
            
        
except KeyboardInterrupt:g
    # Set all servo values to zero when exiting
    for i in range():
        kit.servo[i].angle = 0
    print("Servos set to zero")