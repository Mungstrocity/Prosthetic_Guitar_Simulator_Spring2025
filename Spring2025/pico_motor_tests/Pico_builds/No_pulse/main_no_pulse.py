"""
Basic Motor Control for Raspberry Pi Pico

This is the working build that was able to move the motor when called from command_server.py.
It does not use the pulse function, but instead uses the PWM function to set the speed 
and direction of the motor. This is a snapshot of a working build.

Hardware connections:
- Motor PWM control: GPIO16
- Motor direction pin 1: GPIO14
- Motor direction pin 2: GPIO15

Setup:
    Copy to pico using Thonny. Save as main.py
    Run command_server.py from the computer to send commands to the pico.

Protocol:
    The command format is: move <speed> <duration>
    Example: move 0.5 2.0
    This will run the motor at 50% speed for 2 seconds.
    
Parameters:
    - speed: A float between -1.0 and 1.0, where -1.0 is full speed in one direction, 
             0.0 is stop, and 1.0 is full speed in the other direction.
    - duration: Time in seconds for the motor to run.
    
Behavior:
    The motor will stop automatically after the specified duration.
"""
from machine import Pin, PWM
import sys
import time

class Worm_Motor:
    """
    Motor control class for worm gear motors.
    
    Provides an interface for controlling motor speed and direction
    through PWM and direction pins.
    
    Args:
        pwm_pin (int): GPIO pin number for PWM speed control (default: 16)
        dir_pin1 (int): GPIO pin number for direction control 1 (default: 14)
        dir_pin2 (int): GPIO pin number for direction control 2 (default: 15)
    """
    def __init__(self, pwm_pin=16, dir_pin1=14, dir_pin2=15):
        self.pwm_pin_num = pwm_pin
        self.dir1_pin_num = dir_pin1
        self.dir2_pin_num = dir_pin2

        self.pwm = PWM(Pin(self.pwm_pin_num))
        self.pwm.freq(1000)
        self.pwm.duty_u16(0)
        self.dir1 = Pin(self.dir1_pin_num, Pin.OUT)
        self.dir2 = Pin(self.dir2_pin_num, Pin.OUT)

    def set_speed(self, speed):
        """
        Set the motor speed and direction.
        
        Args:
            speed (float): Speed value between -1.0 and 1.0
                - Negative values run the motor in reverse
                - Positive values run the motor forward
                - 0.0 stops the motor
                
        The function clamps the input value to the valid range [-1.0, 1.0]
        and converts it to the appropriate PWM duty cycle and direction signals.
        """
        speed = max(-1.0, min(1.0, speed))
        self.dir1.value(speed > 0)
        self.dir2.value(speed < 0)
        self.pwm.duty_u16(int(abs(speed) * 65535))

    def stop(self):
        """
        Stop the motor by setting speed to zero and disabling direction pins.
        
        This effectively cuts power to the motor and allows it to coast to a stop.
        """
        self.pwm.duty_u16(0)
        self.dir1.value(0)
        self.dir2.value(0)

    def print_pins(self):
        """
        Print the pin configuration for debugging purposes.
        
        Outputs the GPIO pin numbers used for PWM and direction control
        to the serial console.
        """
        print(f"[DEBUG] PWM pin: GPIO{self.pwm_pin_num}")
        print(f"[DEBUG] DIR1 pin: GPIO{self.dir1_pin_num}")
        print(f"[DEBUG] DIR2 pin: GPIO{self.dir2_pin_num}")

# Initialize the motor control system
motor = Worm_Motor()
motor.print_pins()

# Output confirmation message with unique identifier
print("[DEBUG] CONFIRM-0423C")
print("Motor initialized.")
print("Pico ready.")

# Main command processing loop
while True:
    try:
        # Read commands from REPL input
        cmd = sys.stdin.readline().strip()  # <-- replace input() with this
        print(f"[PICO] Received: {cmd}")
        
        # Parse the command parts
        parts = cmd.split()
        if parts[0] == "move" and len(parts) == 3:
            # Extract speed and duration parameters
            speed = float(parts[1])
            duration = float(parts[2])
            
            # Execute the motor movement
            print(f"[PICO] Running motor at {speed} for {duration} seconds")
            motor.set_speed(speed)
            time.sleep(duration)
            motor.stop()
            print("DONE")
        else:
            print("ERR: Unknown command")
    except Exception as e:
        print(f"ERR: {e}")

