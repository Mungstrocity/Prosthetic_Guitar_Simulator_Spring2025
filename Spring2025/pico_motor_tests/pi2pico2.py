"""
Motor control interface for Raspberry Pi to Raspberry Pico communication.

This script establishes serial communication with a Raspberry Pico microcontroller
and provides functions to send motor movement commands with specified speed and
edge count parameters. The user can interactively input motor control parameters.
"""
import serial
import time

PORT = '/dev/ttyACM0'
BAUD = 115200

def open_serial():
    """
    Establish serial connection to the Pico device.
    
    Returns:
        serial.Serial: An open serial connection to the Pico.
    """
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # wait for Pico to get ready
    return ser

def send_command(ser, command):
    """
    Send a command string to the Pico over serial.
    
    Args:
        ser (serial.Serial): Open serial connection to the Pico.
        command (str): Command to send to the Pico.
    """
    ser.write((command + '\n').encode())
    ser.flush()

def read_response(ser):
    """
    Read and display responses from the Pico until a 'DONE' message is received.
    
    Args:
        ser (serial.Serial): Open serial connection to the Pico.
    """
    while True:
        line = ser.readline().decode().strip()
        if line:
            print("PICO:", line)
            if line == "DONE":
                break

def prompt_and_send():
    """
    Main interactive loop that prompts the user for motor control parameters
    and sends commands to the Pico.
    
    User inputs speed (-1.0 to 1.0) and edge count target for the motor movement.
    """
    ser = open_serial()
    try:
        while True:
            speed = float(input("Enter speed (-1.0 to 1.0): ").strip())
            count = int(input("Enter edge count target: ").strip())

            if speed == 0:
                print("Speed cannot be zero.")
                continue
            if count <= 0:
                print("Edge count must be positive.")
                continue

            cmd = f"move {speed} {count}"
            print(f"Sending: {cmd}")
            send_command(ser, cmd)
            read_response(ser)

    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        ser.close()

if __name__ == "__main__":
    prompt_and_send()
