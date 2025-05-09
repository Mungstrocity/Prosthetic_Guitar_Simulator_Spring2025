"""
Motor Control and Encoder Counting for Raspberry Pi Pico

This script provides motor control functionality with encoder pulse counting
using the PIO state machine on the Raspberry Pi Pico. It is designed to be 
uploaded to a Pico as main.py.

The script implements:
1. A state machine counter for tracking encoder pulses
2. A motor control interface for speed and direction
3. A command interface that accepts speed and duration parameters via serial

Hardware connections:
- Motor PWM control: GPIO16
- Motor direction pin 1: GPIO14
- Motor direction pin 2: GPIO15
- Encoder input A: GPIO22

Usage:
    Upload this file to a Pico as main.py
    Send commands via serial in format: <speed> <duration>
    - speed: float between -1.0 and 1.0
    - duration: time in seconds to run
"""

from machine import Pin, PWM
import sys
import time
import rp2
from rp2 import StateMachine, asm_pio

@asm_pio()
def count_rising_x():
    """
    PIO program to count rising edges on input pin.
    
    This assembly program waits for a rising edge (0->1 transition)
    on the monitored pin and increments the X register each time.
    The count can be read back using the StateMachine interface.
    """
    set(x, 0)
    wrap_target()
    label("loop")
    wait(0, pin, 0)
    wait(1, pin, 0)
    jmp("loop")
    wrap()


class SMCounter:
    """
    State Machine Counter for tracking encoder pulses.
    
    Uses the Raspberry Pi Pico PIO (Programmable I/O) system to efficiently
    count pulses from an encoder without using CPU resources.
    
    Args:
        sm_id (int): State machine ID (0-7)
        input_pin (Pin): Pin object configured as input to monitor
    """
    def __init__(self, sm_id, input_pin):
        self.sm = StateMachine(sm_id, count_rising_x, freq=10_000_000, in_base=input_pin)
        self.sm.active(1)

    def reset(self):
        """Reset the pulse counter to zero."""
        self.sm.active(0)
        self.sm.exec("set(x, 0)")
        self.sm.active(1)
        time.sleep_us(50)

    def value(self):
        """
        Get the current pulse count.
        
        Returns:
            int: Number of pulses counted or -1 if read failed
        """
        self.sm.exec("mov(isr, x)")
        self.sm.exec("push()")
        for _ in range(100):
            if self.sm.rx_fifo():
                return self.sm.get()
            time.sleep_ms(1)
        return -1  # Error signal

    def __del__(self):
        """Clean up by disabling the state machine."""
        self.sm.active(0)


class Worm_Motor:
    """
    Motor control class for worm gear motors with encoder feedback.
    
    Provides an interface for controlling motor speed and direction while
    tracking position using an encoder counter.
    
    Args:
        pwm_pin (int): GPIO pin number for PWM speed control
        dir_pin1 (int): GPIO pin number for direction control 1
        dir_pin2 (int): GPIO pin number for direction control 2
        enc_a (int): GPIO pin number for encoder channel A
    """
    def __init__(self, pwm_pin=16, dir_pin1=14, dir_pin2=15, enc_a=22):
        self.pwm_pin_num = pwm_pin
        self.dir1_pin_num = dir_pin1
        self.dir2_pin_num = dir_pin2
        self.enc_pin_num = enc_a

        self.pwm = PWM(Pin(self.pwm_pin_num))
        self.pwm.freq(1000)
        self.pwm.duty_u16(0)
        self.dir1 = Pin(self.dir1_pin_num, Pin.OUT)
        self.dir2 = Pin(self.dir2_pin_num, Pin.OUT)

        self.encoder = SMCounter(0, Pin(enc_a, Pin.IN))

    def reset_position(self):
        """Reset the encoder position counter to zero."""
        self.encoder.reset()

    def get_position(self):
        """
        Get the current encoder position.
        
        Returns:
            int: Current encoder pulse count or -1 if read failed
        """
        return self.encoder.value()

    def set_speed(self, speed):
        """
        Set the motor speed and direction.
        
        Args:
            speed (float): Speed value between -1.0 and 1.0
                - Negative values run the motor in reverse
                - Positive values run the motor forward
                - 0.0 stops the motor
        """
        speed = max(-1.0, min(1.0, speed))
        self.dir1.value(speed > 0)
        self.dir2.value(speed < 0)
        self.pwm.duty_u16(int(abs(speed) * 65535))

    def stop(self):
        """Stop the motor by setting speed to zero and disabling direction pins."""
        self.pwm.duty_u16(0)
        self.dir1.value(0)
        self.dir2.value(0)

    def print_pins(self):
        """Print the pin configuration for debugging purposes."""
        print(f"[DEBUG] PWM pin:  GPIO{self.pwm_pin_num}")
        print(f"[DEBUG] DIR1 pin: GPIO{self.dir1_pin_num}")
        print(f"[DEBUG] DIR2 pin: GPIO{self.dir2_pin_num}")
        print(f"[DEBUG] READ pin: GPIO{self.enc_pin_num}")


# Initialize the motor control system
motor = Worm_Motor()
motor.print_pins()

print("[DEBUG] CONFIRM-0423P")
print("Motor initialized.")
print("Pico ready.")

# Main command processing loop
while True:
    try:
        cmd = sys.stdin.readline().strip()
        print(f"[PICO] Received: {cmd}")
        parts = cmd.split()
        if len(parts) == 2:
            speed = float(parts[0])
            duration = float(parts[1])
            motor.reset_position()
            print(f"[PICO] Running motor at {speed} for {duration} seconds")
            motor.set_speed(speed)
            print("[PICO] going to SLEEP...")
            time.sleep(duration)
            print("[PICO] sending STOP...")
            motor.stop()
            print("[PICO] send GET_POSITION()...")
            count = motor.get_position()
            if count == -1:
                print("[PICO] ERROR: Failed to get encoder count.")
            else:
                print(f"[PICO] DONE. Encoder pulses: {count}")
        else:
            print("ERR: Expected two numbers: <speed> <duration>")
    except Exception as e:
        print(f"ERR: {e}")

