from flask import Flask, request, jsonify
from gui import gui_launch
from finger_control import fret_note
from angles import get_angles
from pressure import read_pressure
import random
import sys
import time

app = Flask(__name__)

random_flag = False  # Define random_flag as a global variable
message = ""  # Initialize an empty message

#define voltage and pressure cutoffs
max_calibrated = 12.0
max_allowed = 2.0
max_volts = 3.0
voltage_cutoff = (max_calibrated / max_allowed) * max_volts

pressure_v = read_pressure()

@app.route('/handle_gui_data', methods=['POST'])
def handle_gui_data():
    global random_flag, message  # Access the global variables
    data = request.get_json()
    state = data.get('state')
    string_num = data.get('string_num')
    duration = data.get('duration')

    print(f"roboGuitar, {state}, {string_num}, {duration}")  # Debugging output

    if state == "exit":
        message = "Exiting application."
        print(message)
        sys.exit(0)
    elif state == "get_angles":
        print(f"roboGuitar, {state}, {string_num}")  # Debugging output
        state, angles = get_angles(string_num, 1)
        print(f"roboGuitar, {state}, {angles}")  # Debugging output
        state = fret_note(angles, duration, finger=1)
        if pressure_v > voltage_cutoff:  # Basic interrupt for pressure
            message = "Pressure exceeded. Exiting application."
            print(message)
            sys.exit(0)
        else:
            message = f"Playing string {string_num} on fret 1 for {duration} seconds"
    elif state == "random":
        random_flag = True
        while random_flag:
            string_num = random.randint(0, 6)
            print(f"roboGuitar-random, {state}, {string_num}, {duration}")  # Debugging output
            angles = get_angles(string_num, fret_number=1)
            fret_note("angles acquired", angles, duration, finger=1)
            print(f"roboGuitar-random, angles acquired, {angles}")
            if string_num == 0:
                message = f"Playing open for {duration} seconds"
            else:
                message = f"Playing string {string_num} on fret 1 for {duration} seconds"
            print(f"Message: {message}")
            if not random_flag:
                break

    return jsonify({"status": "success", "message": message})

@app.route('/handle_gui_data', methods=['GET'])
def test_connection():
    return jsonify({"status": "Server is running"}), 200

@app.route('/get_message', methods=['GET'])
def get_message():
    global random_flag
    string_num = request.args.get('string_num', type=int)
    duration = request.args.get('duration', type=float)

    if string_num == 0:
        message = f"Playing open for {duration} seconds"
    else:
        message = f"Playing string {string_num} on fret 1 for {duration} seconds"

    return jsonify({"message": message})

# Update random mode logic to send messages
def handle_random_mode():
    global random_flag
    while random_flag:
        string_num = random.randint(0, 6)
        duration = random.uniform(1, 5)  # Random duration between 1 and 5 seconds
        print(f"roboGuitar-random, Playing string {string_num} for {duration} seconds")

        # Generate angles and fret note
        angles = get_angles(string_num, fret_number=1)
        fret_note("angles acquired", angles, duration, finger=1)

        # Send message
        if string_num == 0:
            message = f"Playing open for {duration} seconds"
        else:
            message = f"Playing string {string_num} on fret 1 for {duration} seconds"
        print(f"Message: {message}")

        # Simulate delay for the duration
        time.sleep(duration)

        if not random_flag:
            break

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)