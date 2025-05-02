import serial
import time

PORT = '/dev/ttyACM0'
BAUD = 115200

def open_serial():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    time.sleep(2)  # wait for Pico to get ready
    return ser

def send_command(ser, command):
    ser.write((command + '\n').encode())
    ser.flush()

def read_response(ser):
    while True:
        line = ser.readline().decode().strip()
        if line:
            print("PICO:", line)
            if line == "DONE":
                break

def prompt_and_send():
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
