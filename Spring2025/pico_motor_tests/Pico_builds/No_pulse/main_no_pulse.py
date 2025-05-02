"""This is the working build that was able to move the motor when called from command_server.py
   It does not use the pulse function, but instead uses the PWM function to set the speed 
   and direction of the motor. This is a snapshot of a working build
   Copy to pico using Thonny. Save as main.py
   Run command_server.py from the computer to send commands to the pico.
   The command format is: move <speed> <duration>
   Example: move 0.5 2.0
   This will run the motor at 50% speed for 2 seconds.
   The speed can be between -1.0 and 1.0, where -1.0 is full speed in one direction, 0.0 is stop, and 1.0 is full speed in the other direction.
   The duration is in seconds.
   The motor will stop after the duration is over.
                                                 """
from machine import Pin, PWM
import sys
import time

class Worm_Motor:
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
        speed = max(-1.0, min(1.0, speed))
        self.dir1.value(speed > 0)
        self.dir2.value(speed < 0)
        self.pwm.duty_u16(int(abs(speed) * 65535))

    def stop(self):
        self.pwm.duty_u16(0)
        self.dir1.value(0)
        self.dir2.value(0)

    def print_pins(self):
        print(f"[DEBUG] PWM pin: GPIO{self.pwm_pin_num}")
        print(f"[DEBUG] DIR1 pin: GPIO{self.dir1_pin_num}")
        print(f"[DEBUG] DIR2 pin: GPIO{self.dir2_pin_num}")

motor = Worm_Motor()
motor.print_pins()

print("[DEBUG] CONFIRM-0423C")
print("Motor initialized.")
print("Pico ready.")

while True:
    try:
        cmd = sys.stdin.readline().strip()  # <-- replace input() with this
        print(f"[PICO] Received: {cmd}")
        parts = cmd.split()
        if parts[0] == "move" and len(parts) == 3:
            speed = float(parts[1])
            duration = float(parts[2])
            print(f"[PICO] Running motor at {speed} for {duration} seconds")
            motor.set_speed(speed)
            time.sleep(duration)
            motor.stop()
            print("DONE")
        else:
            print("ERR: Unknown command")
    except Exception as e:
        print(f"ERR: {e}")

