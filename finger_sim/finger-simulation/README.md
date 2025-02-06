# Finger Simulation

This project is a 2D visual simulation of a finger, designed to demonstrate inverse kinematics for positioning the tip of the finger to fret a string on a guitar. The finger is represented as a series of segments (bars) that articulate at joints.

## Project Structure

```
finger-simulation
├── src
│   ├── main.py               # Entry point of the simulation
│   ├── inverse_kinematics.py # Contains the InverseKinematics class
│   ├── finger.py             # Defines the Finger class
│   └── utils.py              # Utility functions for calculations and rendering
├── requirements.txt          # Lists project dependencies
└── README.md                 # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/finger-simulation.git
   cd finger-simulation
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the simulation, execute the following command:
```
python src/main.py
```

## Features

- Visual representation of a finger with articulated joints.
- Inverse kinematics calculations to position the finger tip accurately.
- User input handling to interactively place the finger tip on a virtual guitar string.

## Acknowledgments

This project utilizes various libraries for graphical rendering and mathematical calculations. Please refer to the `requirements.txt` for a complete list of dependencies.