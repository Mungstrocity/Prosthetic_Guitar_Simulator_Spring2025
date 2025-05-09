"""
Angle calculation module for robotic guitarist finger positioning.

This module provides functionality to determine appropriate finger angles
for playing different frets on different strings of a guitar.
Angles are retrieved from a CSV file containing pre-calculated values.
"""

import csv
import os

BASE_DIR = os.path.dirname(__file__)

def get_angles(string_number: int, fret_number: int) -> tuple:
    """
    Calculate the angles for a given string and fret number.

    Args:
        string_number (int): The string number (1-6).
        fret_number (int): The fret number (0-24).

    Returns:
        tuple: A tuple containing the angles (prox, med, dist, abd).
    """
    print(f'get_angles {string_number} {fret_number}')
    # Constants
    NEUTRAL = [180, 180, 180, 0]
    state = "angles_acquired"
    
    if fret_number == 0:
        return state, NEUTRAL

    # Read angles from CSV
    csv_path = os.path.join(BASE_DIR, "assets", "data", "angles.csv")
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)  # Use DictReader for column-based access
        for row in reader:
            if int(row['fret_number']) == fret_number and int(row['string_number']) == string_number:
                prox, med, dist, abd = map(float, (row['prox'], row['med'], row['dist'], row['abd']))
                angles = [prox, med, dist, abd]
                state = "angles acquired"
                return state, angles

    # Default to NEUTRAL if no match is found
    return state, NEUTRAL