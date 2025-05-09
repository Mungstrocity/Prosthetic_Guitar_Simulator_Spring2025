"""
Command Server for Raspberry Pi to Pico Motor Control System

This script runs on a Raspberry Pi or computer and sends motor control commands
to a connected Raspberry Pi Pico over a serial connection. It provides a simple
command-line interface for sending speed and duration parameters to control
motor movements.

Usage:
    Run this script and enter commands in the format: <speed> <duration>
    Where:
        - speed: A float value between -1.0 and 1.0
        - duration: Time in seconds for the motor to run

Example:
    > 0.5 2.0    (Run motor at 50% speed for 2 seconds)
    > -0.75 1.5  (Run motor at 75% speed in reverse for 1.5 seconds)
    > exit       (Quit the program)
"""
import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

def send_command(speed, duration):
    """
    Sends a motor control command to the Pico over serial and waits for completion.
    
    Args:
        speed (float): Motor speed from -1.0 to 1.0
        duration (float): Duration to run the motor in seconds
        
    The function blocks until the Pico responds with "DONE" or an error message.
    All communication with the Pico is logged to the console.
    """
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
        cmd = f"{speed} {duration}\n"
        print(f"[PI] Sending: {cmd.strip()}")
        ser.write(cmd.encode())

        while True:
            try:
                line = ser.readline()
                if not line:
                    continue  # just wait for more input

                decoded = line.decode().strip()
                if decoded:
                    print(f"[PICO] {decoded}")

                if decoded.startswith("[PICO] DONE") or "ERROR" in decoded:
                    break
            except UnicodeDecodeError:
                print(f"[PICO] [RAW] {repr(line)}")

def main():
    """
    Main function that provides a command-line interface for sending motor commands.
    
    Continuously prompts user for input until "exit" is entered.
    Input should be two space-separated numbers: speed and duration.
    """
    print("Motor Command Server Ready.")
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == "exit":
                break

            parts = user_input.split()
            if len(parts) != 2:
                print("ERR: Enter two numbers: <speed> <duration>")
                continue

            speed = float(parts[0])
            duration = float(parts[1])
            send_command(speed, duration)

        except KeyboardInterrupt:
            break
        except ValueError:
            print("ERR: Invalid numeric input")

if __name__ == "__main__":
    main()