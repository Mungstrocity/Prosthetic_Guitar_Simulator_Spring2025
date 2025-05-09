# Prosthetic_Guitar_Simulator SPRING2025
## Motor Tests
These files were built to test control of the motors. They were used to establish the general control scheme used in the main control file.

## Pico Motor Tests
These were the files built to attempt to control the DC motor and read the position data from the quadrature encoders. The Pico was selected because it is equipped with 4 state machines that can be programmed using proprietary assembly code. They are able to read signals at extremely high frequencies without taxing the main processor. Control of the motor was successful but reading the signal was not.
The pico_builds directory contains the most recent working state that moved the motor successfully. The command_server.py file is intended to be the control file for the dc motor. Once the motor is configured so that it can command movement (done) and read accurate positional data (not done), it can then be configured to receive signals from the finger_control.py module.

## Main application
The robo_guitarist directory contains what is inteded to be the complete demo application. roboGuitar.py functions as the core file and server. It must be run first. remote_gui.py can be run on the same computer or on any other device on the same network. roboGuitar.py must be running before the GUI can connect. The IP address of the Raspberry pi will need to be entered manually into the code for the GUI if it changes. This will no longer be an issue once a static IP is obtained. Follow up with CEAT IT on ticket number 24325 to finalize the static IP allocation.


# Prosthetic_Guitar_Simulator FALL2024
## Node Distance Tool for Godot

The Node Distance Tool is an addon that simplifies measuring distances between 3D nodes directly in the Godot editor. Using it, you can select two nodes with the Q key and measure the distance between them, displaying the values directly in the scene and console.

### How It Works
Quick Selection with "Q": Select a node with the mouse and press Q to register it. Then, select another node and press Q again to measure the distance between them. The distance will be displayed in the scene and the console (print_rich).

![print_rich](https://github.com/user-attachments/assets/d16f1619-196c-41c7-b6eb-6c6d461ed6c9)

### Measurement Modes
This addon has three distinct modes for measurement:

#### Normal Mode: Select two nodes with "Q" to measure the distance. It creates a line connecting the nodes and displays a label with the rounded distance. After measuring two nodes, you need to select two more for the next measurement. Ideal for direct, precise measurements, with all calculations displayed in the console.

![Normal](https://github.com/user-attachments/assets/7b2a3e40-42ed-43fc-bc88-cc54ff11cd3d)

#### Continuos Mode: After measuring two nodes, the next selected node will automatically be measured in relation to the previous one. This allows for continuous sequences of measurements without resetting.

![Continuos](https://github.com/user-attachments/assets/20d1e2b7-1c35-40e9-95b6-43bcb7d72d17)

#### Togheter Mode: Select multiple nodes with "Q", and when any of them move, the distance between all nodes is recalculated and displayed. Previous lines and labels are updated to reflect the new distances. All calculations are displayed in the console.

![Togheter](https://github.com/user-attachments/assets/03c706b3-90f4-4dd7-a86c-eab3890f8a29)

### Control Panel
In the 3D editor, there is a control panel located in the CONTAINER_SPATIAL_EDITOR_MENU (PainelMetragem) that facilitates activating the modes and visualizing measurements. The buttons include:

Reset: Removes all measurements from the scene.
Show/Hide Lines and Labels: Toggles the display of lines and labels.
Continuos and Togheter Modes: Activates or deactivates these modes directly from the panel.

![buttons](https://github.com/user-attachments/assets/25110eb6-6b05-4788-8eb5-45fe1ebfe316)

### License
This project is licensed under the terms described in the LICENSE file.

# Prosthetic_Guitar_Simulator SPRING2024
Oklahoma State University Senior Design project

## Clone the repo
```
git clone https://github.com/Thomas-J-Kidd/Prosthetic_Guitar_Simulator.git
```

## Downloading the model
Make sure that the model is present in in the `fretHand` folder

Your directory should look something like this using the `ls` command

```
⚡➜ fretHand (U main) ls
MANO  mano_v1_2
```


## Running the demo program for creating a 3D hand

1) Nagivate to the correct folder
```Prosthetic_Guitar_Simulator/3d_modelling/fretHand/MANO```

You can verify you are in the right place by using the `pwd` command

2) install the pyhon virtual environment

### Linux

*Install virtualenv if you haven't already*
```sudo apt-get install python3-venv```

*Create a virtual environment*
```python3 -m venv myenv```

*Activate the virtual environment*
```source myenv/bin/activate```


### Windows
*Install virtualenv if you haven't already*
```pip install virtualenv```

*Create a virtual environment*
```virtualenv myenv```

*Activate the virtual environment*
```myenv\Scripts\activate```

3) Install the python libraries
```pip install requirements.txt```

4) Run demo.py

Run the code by using `python demo.py`

5) Deactivate the environment

```deactivate```

# Repo Diagram
```
Prosthetic_Guitar_Simulator_Spring2025/
├── LICENSE
├── README.md
├── teambig_workspace.code-workspace
├── PREVIOUS_SEMESTERS/
│   ├── blender/
│   │   └── playerModelRiggedforBlender.glb
│   │ 
│   ├── CadenCV/
│   │   ├── __init__.py
│   │   ├── bar.py
│   │   ├── best_match.py
│   │   ├── box.py
│   │   ├── main.py
│   │   ├── midi2xml.py
│   │   ├── primitive.py
│   │   ├── README.md
│   │   ├── Requirements.txt
│   │   ├── staff.py
│   │   ├── output/
│   │   └── resources/
│   │ 
│   ├── cadenCV_Fall2024/
│   │   ├── bar.py
│   │   ├── best_match.py
│   │   ├── box.py
│   │   ├── image_to_text.py
│   │   ├── main.py
│   │   ├── primitive.py
│   │   ├── README.md
│   │   ├── staff.py
│   │   ├── output/
│   │   └── resources/
│   │ 
│   ├── finger_sim/
│   │   ├── finger-simulation/
│   │   └── finger-simulation-v2/
│   │ 
│   ├── modelling_3d/
│   │   ├── __init__.py
│   │   ├── coordinateTesting.py
│   │   ├── FINALMODEL.obj
│   │   ├── Guitar1.obj
│   │   ├── Guitar2.obj
│   │   ├── objLoad.py
│   │   ├── stringsFrets.txt
│   │   ├── fretHand/
│   │   └── models_compressed/
│   │ 
│   ├── models_compressed/
│   │   ├── Guitar2.bam
│   │   └── guitarModel.bam
│   │ 
│   ├── musicExampleFiles/
│   │   └── BossSilentNight/
│   │ 
│   ├── musicXML_Files/
│   │   ├── Fire Emblem.xml
│   │   ├── Kookaburra.xml
│   │   ├── Mary.xml
│   │   ├── output.musicxml
│   │   ├── Probably Wrong.xml
│   │   ├── score.musicxml
│   │   ├── Teapot.xml
│   │   └── Twinkle.xml
│   │ 
│   ├── NoteResources/
│   │   └── NoteClefDiagram.png
│   │ 
│   ├── position_mapping/
│   │   ├── __init__.py
│   │   ├── linux_musicClasses.py
│   │   ├── main.py
│   │   ├── moduleTester.py
│   │   ├── musicClasses.py
│   │   ├── README.md
│   │   ├── XMLInterpret.py
│   │   ├── xmlreference.txt
│   │   ├── __pycache__/
│   │   └── staticData/
│   │ 
│   ├── prosthetic_guitar_simulator/
│   │   ├── animation_player.gd
│   │   ├── animation_tester.gd
│   │   ├── gui_control.gd
│   │   ├── gui_control.tscn
│   │   ├── guitar_player.gd
│   │   ├── guitar.gd
│   │   ├── Guitar.tscn
│   │   ├── guitarModel.bam
│   │   ├── GuitarPlayer.tscn
│   │   ├── GuitarSounds.tscn
│   │   ├── icon.svg
│   │   ├── ik_target_finger.gd
│   │   ├── ik.gd
│   │   ├── input.xml
│   │   ├── LICENSE
│   │   ├── main_3d_scene.gd
│   │   ├── Main3dScene.tscn
│   │   ├── music_xml_parser_test.gd
│   │   ├── note_player.gd
│   │   ├── project.godot
│   │   ├── README.md
│   │   ├── xmlParser.gd
│   │   ├── addons/
│   │   ├── Assets/
│   │   └── Exe/
│   │ 
│   └── skeleton_code_examples/
│       ├── Sample_dataclass.py
│       ├── sample_dictionary.py
│       └── Sample_KeySig.yaml
│   
└── SPRING2025/
    ├── motor_tests/
    │   └── src/
    │       ├── cont_motor.py
    │       ├── encoder_data_count_based_pulse_20250418_122152.csv
    │       ├── encoder_data_count_based_pulse_20250418_122257.csv
    │       ├── encoder_data_count_based_pulse_20250422_110935.csv
    │       ├── i2cTest.py
    │       ├── motorcontrol10.py
    │       ├── PICO Pinout.svg
    │       ├── pico_pinout.txt
    │       ├── rpi5 pinout.jpg
    │       ├── servo_static_calibration.py
    │       ├── signal_reader.py
    │       ├── wormgear_test.py
    │       ├── worm_gpiozero.py
    │       ├── worm_gpiozero_freq_test.py
    │       ├── worm_gpiozero_interrupt.py
    │       ├── worm_gpiozero_interrupt_count_based_pulse.py
    │       └── worm_gpiozero_interrupt_pulse.py
    │
    ├── pico_motor_tests/
    │   ├── command_server.py
    │   ├── pi2pico2.py
    │   ├── pi_to_pico_motor_test.py
    │   └── Pico_builds/
    │       └── No_pulse/
    │           ├── command_server.py
    │           ├── main_no_pulse.py
    │           └── pico.py
    │
    └── robo_guitarist/
        ├── angles.py
        ├── finger_control.py
        ├── gui.py
        ├── i2c_shared.py
        ├── pressure.py
        ├── remote_gui.py
        ├── roboGuitar.py
        └── assets/
            ├── data/
            └── images/
```
