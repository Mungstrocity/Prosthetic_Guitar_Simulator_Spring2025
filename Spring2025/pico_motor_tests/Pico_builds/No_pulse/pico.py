#COPY INTO PICO AS main.py

from machine import Pin, PWM
import sys
import time
import rp2
from rp2 import StateMachine, asm_pio
"""
This is a test file to read just the pulse data from any encoder. It does not work yet.
It will be used to validate the state machine counter.
"""

# PIO: Count rising edges on GPIO10 by incrementing X
@asm_pio()
def count_rising_x():
    set(x, 0)
    wrap_target()
    label("loop")
    wait(0, pin, 0)
    wait(1, pin, 0)
    jmp("loop")
    wrap()

class SMCounter:
    def __init__(self, sm_id, input_pin):
        self.sm = StateMachine(sm_id, count_rising_x, freq=10_000_000, in_base=input_pin)
        self.sm.active(1)

    def reset(self):
        self.sm.active(0)
        self.sm.exec("set(x, 0)")
        self.sm.active(1)
        time.sleep_us(50)

    def value(self):
        self.sm.exec("mov(isr, x)")
        self.sm.exec("push()")
        for _ in range(100):
            if self.sm.rx_fifo():
                return self.sm.get()
            time.sleep_ms(1)
        return -1  # Error signal

    def __del__(self):
        self.sm.active(0)

class Worm_Motor:
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
        self.encoder.reset()

    def get_position(self):
        return self.encoder.value()

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
        print(f"[DEBUG] PWM pin:  GPIO{self.pwm_pin_num}")
        print(f"[DEBUG] DIR1 pin: GPIO{self.dir1_pin_num}")
        print(f"[DEBUG] DIR2 pin: GPIO{self.dir2_pin_num}")
        print(f"[DEBUG] READ pin: GPIO{self.enc_pin_num}")

motor = Worm_Motor()
motor.print_pins()

print("[DEBUG] CONFIRM-0423P")
print("Motor initialized.")
print("Pico ready.")

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

