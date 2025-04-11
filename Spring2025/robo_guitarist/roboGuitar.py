from flask import Flask, request, jsonify
from gui import gui_launch
from finger_control import fret_note
from angles import get_angles
from pressure import read_pressure
import random
import sys

app = Flask(__name__)

random_flag = False  # Define random_flag as a global variable

#define voltage and pressure cutoffs
max_calibrated = 12.0
max_allowed = 2.0
max_volts = 3.0
voltage_cutoff = (max_calibrated / max_allowed) * max_volts

pressure_v = read_pressure()

@app.route('/handle_gui_data', methods=['POST'])
def handle_gui_data():
    global random_flag  # Access the global random_flag variable
    data = request.get_json()
    state = data.get('state')
    string_num = data.get('string_num')
    duration = data.get('duration')

    print(f"roboGuitar, {state}, {string_num}, {duration}")  # Debugging output

    if state == "exit":
        print("Exiting application.")
        sys.exit(0)
    elif state == "get_angles":
        print(f"roboGuitar, {state}, {string_num}")  # Debugging output
        state, angles = get_angles(string_num, 1)
        print(f"roboGuitar, {state}, {angles}")  # Debugging output
        state = fret_note(angles, duration)
        if pressure_v > voltage_cutoff: # basic interrupt for pressure
            print("Pressure exceeded. Exiting application.")
            sys.exit(0)
    elif state == "random":
        random_flag = True
        while random_flag:
            string_num = random.randint(0, 6)
            print(f"roboGuitar-random, {state}, {string_num}, {duration}")  # Debugging output
            angles = get_angles(string_num, fret_number=1)
            fret_note("angles acquired", angles, duration, finger=1)
            print(f"roboGuitar-random, angles acquired, {angles}")
            if random_flag == False:
                break

    return jsonify({"status": "success"})

@app.route('/handle_gui_data', methods=['GET'])
def test_connection():
    return jsonify({"status": "Server is running"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)