from adafruit_servokit import ServoKit
from gpiozero import PWMOutputDevice, DigitalOutputDevice
import time
import time

NEUTRAL = [180, 180, 180, 0]
current_angles = [0,0,0,0]

def fret_note(angles, duration, finger):
    """
    Fret a note by moving the fingers to the specified angles.
    
    Args:
        angles (list): A list of angles for each finger joint.
    """
    # Code to control the robot's fingers to fret a note
    
    prox_motor, prox_angle, servos, servo_angles = motor_assign(finger)
    worm_motor_control(prox_motor, prox_angle)
    servo_motor_control(servos, servo_angles)
    
    print(f"pausing for {duration} seconds")
    
    
    time.sleep(duration)
    print(f"fret_note,{angles},{duration}")

def motor_assign(finger, angles):
    """
    Assign a motor index to a finger.
    
    Args:
        finger (int): The finger number (0 - 4).
    
    Returns:
        int: The assigned motor numbers.
        worm gear motors 1 - 4
        servo motors 1 - 12
    """
    # Code to assign a motor to the specified finger
    if finger < 0 or finger > 4:
        raise ValueError("Finger number must be between 0 and 4.")

    # Servo assigments
    prox = finger
    med = finger + ((finger - 1) * 3)
    dist = med + 1
    abd = dist + 1
    
    print(f'motor_assign,{finger},{prox},{med},{dist},{abd}')
    
    return prox, angles[0], [med, dist, abd], [angles[1], angles[2], angles[3]]
    
def servo_motor_control(servos, servo_angles):
    """
    Control the servo motors to move to the specified angles.
    
    Args:
        servos (list): A list of servo motor numbers.
        angles (list): A list of angles for each servo motor.
    """
    # Code to control the servo motors
    kit = ServoKit(channels=16)
    
    for i in range(len(servos)):
        kit.servo[servos[i]].angle = servo_angles[i]
        print(f"servo {servos[i]} set to {servo_angles[i]} degrees")
        
    current_angles[1:4] = servo_angles #set current angle for comparison
    print(f"servo_motor_control,{servos},{servo_angles},{current_angles}")
    
def worm_motor_control(prox_motor, prox_angle):
    """
    Control the worm gear motor to move to the specified angle.
    
    Args:
        prox_motor (int): The worm gear motor number.
        prox_angle (int): The angle for the worm gear motor.
    """
    # Define GPIO Pins (BCM mode)
    # IN1 = 17  # Motor direction
    # IN2 = 27  # Motor direction


    # ENC_A = 23  # Encoder A signal
    # ENC_B = 24  # Encoder B signal
    # ENA = 18
    
    # freq = 1000  # PWM frequency, works best at 1k or 2k Hz
    # ena.value = 1

    # # Initialize GPIO devices
    # in1 = DigitalOutputDevice(IN1)
    # in2 = DigitalOutputDevice(IN2)
    # ena = PWMOutputDevice(ENA, frequency=freq)
    
    speed = 1

    

    angle_conversion_factor = 1
    angle_2_count = abs(prox_angle - current_angles[0]) * angle_conversion_factor
    
    count_ref_current = []
    count = 0
    
    # while count < angle_2_count:
        # Read encoder values
        # count_ref = [DigitalOutputDevice(ENC_A).value, DigitalOutputDevice(ENC_B).value]
    count_ref = [0, 0]  # Placeholder for encoder values
    if count_ref_current == []:
        count_ref_current = count_ref
    if count_ref != count_ref_current:
        count_ref_current = count_ref
        count += 1
    
    if prox_angle > current_angles[0]:
        # Set the direction to forward
        # in1.on()
        # in2.off()
        print("forward")
    else:
        # Set the direction to reverse
        # in1.off()
        # in2.on()
        print("reverse")
    print(f"worm_motor_control,{prox_motor},{prox_angle},{speed},{count},{count_ref_current}")
    """Stop motor."""
    # ena.value = 0  # Disable motor
    speed = 0
    print(f"worm_motor_control,{prox_motor},{prox_angle},{speed},{count},{count_ref_current}")
        
        
            