"""
Command server for Raspberry Pi to Pico communication.

This script creates a simple command server that allows sending arbitrary
commands to a connected Raspberry Pico microcontroller over a serial connection.
Commands are entered by the user and sent to the Pico, with responses displayed
until a 'DONE' message is received.

Note: This script assumes the Pico is connected at /dev/ttyACM0 on Linux.
For Windows, the port should be changed to a COM port (e.g., 'COM3').
"""
import serial

SERIAL_PORT = "/dev/ttyACM0"
BAUD_RATE = 115200

def send_command(command):
    """
    Send a command to the Pico and display its responses.
    
    Opens a serial connection, sends the provided command string to the Pico,
    and prints all response lines until a 'DONE' message is received or the
    connection times out.
    
    Args:
        command (str): The command string to send to the Pico.
    """
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2) as ser:
        print(f"[PI] Sending: {command}")
        ser.write((command + "\n").encode())

        while True:
            line = ser.readline().decode().strip()
            if not line:
                break
            print(f"[PICO] {line}")
            if line == "DONE":
                break

def main():
    """
    Main function that provides an interactive command prompt.
    
    Continuously prompts for user commands and sends them to the Pico
    until the user enters 'exit' or interrupts with Ctrl+C.
    """
    print("Motor Command Server Ready.")
    while True:
        try:
            cmd = input("> ")
            if cmd.lower() == "exit":
                break
            send_command(cmd)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
