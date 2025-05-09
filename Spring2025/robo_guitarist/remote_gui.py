"""
Remote GUI for controlling a robotic guitarist.

This module provides a graphical interface for controlling a robotic guitarist remotely.
It allows users to select strings, set durations, and submit commands to a server.
The application supports both manual control and a random mode.

Make sure that roboGuitar.py is running then launch this file.
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter.ttk import Combobox
import requests

BASE_DIR = os.path.dirname(__file__)

# Global state variables
state_vars = {
    "state": "not_started",
    "selected_button": None,
    "duration": None,
    "string_num": None,
    "active_button": None,
}

def notify_blocked_input(event=None):
    """
    Display a notification when inputs are blocked in random mode.
    
    Args:
        event: Optional tkinter event object
    """
    if state_vars["state"] == "random":
        messagebox.showinfo("Random Mode Active", "Inputs are blocked while in Random Mode. Exit Random Mode to continue.")

def update_status(message):
    """
    Update the status label with the provided message.
    
    Args:
        message (str): The status message to display
    """
    status_text.set(message)

def send_data_to_server(state, string_num, duration):
    """
    Send control data to the robotic guitarist server.
    
    Args:
        state (str): Current state of the application
        string_num (int): Selected string number (0-6)
        duration (float): Duration in seconds
    
    Returns:
        None
    """
    server_ip = "10.228.12.158"  # IP address of the server
    server_url = f"http://{server_ip}:5000/handle_gui_data"

    data = {
        "state": state,
        "string_num": string_num,
        "duration": duration
    }

    try:
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("Data sent successfully to the server.")
        else:
            print(f"Failed to send data to the server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the server: {e}")

def test_server_connection():
    """
    Test the connection to the robotic guitarist server.
    
    Prints a message indicating success or failure of the connection attempt.
    """
    server_ip = "10.228.12.158"  # IP address of the server
    server_url = f"http://{server_ip}:5000/handle_gui_data"

    try:
        response = requests.get(server_url)
        if response.status_code == 200:
            print("Successfully connected to the server.")
        else:
            print(f"Server connection failed. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the server: {e}")

def fetch_message_from_server(string_num, duration):
    """
    Fetch a message from the server based on string number and duration.
    
    Args:
        string_num (int): Selected string number (0-6)
        duration (float): Duration in seconds
    
    Returns:
        str: Message received from the server or error message
    """
    server_ip = "10.228.12.158"  # IP address of the server
    server_url = f"http://{server_ip}:5000/get_message"

    params = {
        "string_num": string_num,
        "duration": duration
    }

    try:
        response = requests.get(server_url, params=params)
        if response.status_code == 200:
            message = response.json().get("message", "")
            print(f"Message from server: {message}")
            return message
        else:
            print(f"Failed to fetch message from server. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to the server: {e}")

    return "Error fetching message from server"

def on_button_click(button_id, button_widgets):
    """
    Handle string selection button click events.
    
    Args:
        button_id (int): ID of the clicked button (0-6)
        button_widgets (dict): Dictionary of button widgets
    """
    global state_vars
    if state_vars["state"] == "random":
        notify_blocked_input()  # Notify if inputs are blocked
        return

    selected_button, active_button = state_vars["selected_button"], state_vars["active_button"]
    state_vars["selected_button"] = button_id

    if active_button:
        active_button.config(relief=tk.RAISED)

    state_vars["active_button"] = button_widgets[button_id]
    state_vars["active_button"].config(relief=tk.SUNKEN)

def on_duration_submit(duration_var):
    """
    Process duration submission.
    
    Args:
        duration_var (StringVar): Tkinter variable containing duration text input
    
    Updates state variables based on user input and displays status message.
    Shows error messages for invalid inputs.
    """
    global state_vars
    try:
        duration_value = float(duration_var.get())
        if duration_value > 0 and state_vars["selected_button"] is not None:
            state_vars["string_num"], state_vars["duration"] = state_vars["selected_button"], duration_value
            update_status(f"Playing fret 1 on string {state_vars['string_num']} for {state_vars['duration']:.1f} seconds")
            if state_vars["active_button"]:
                state_vars["active_button"].config(relief=tk.RAISED)
                state_vars["active_button"] = None
            state_vars["selected_button"] = None
            duration_var.set("")
            state_vars["state"] = "get_angles"
            print(f"Submitted: {state_vars}")
        else:
            messagebox.showerror("Invalid Submission", "Please select a string nubmer and enter a duration greater than 0.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid float value for duration.")

def gui_launch(random_flag, on_data_submit):
    """
    Launch the Robo Guitarist GUI.
    
    Args:
        random_flag (bool): Whether to start in random mode
        on_data_submit (function): Callback function executed when data is submitted.
                                  Takes three arguments: state, string_num, and duration
    
    Returns:
        None
    
    This function creates and displays the main GUI window with all controls,
    including string selection buttons, duration input, and mode toggles.
    The GUI runs until the window is closed.
    """
    global state_vars, status_text
    state_vars["state"] = "ready" if not random_flag else "random"

    # Test server connection
    test_server_connection()

    root = tk.Tk()
    root.title("Robo Guitarist")
    root.geometry("1024x576")

    def on_exit_click():
        """Handle the exit button click or window close event."""
        state_vars["state"] = "exit"
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_exit_click)

    # Load background image
    bg_image_path = os.path.join(BASE_DIR, "assets", "images", "GUI3.png")
    bg_image = Image.open(bg_image_path).resize((1024, 576), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)
    bg_label.image = bg_photo

    # Controls frame
    controls_frame = tk.Frame(root, padx=10, pady=10)
    controls_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20, anchor="n")

    # String selection buttons
    button_frame = tk.LabelFrame(controls_frame, text="Select a string", padx=10, pady=10)
    button_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    button_widgets = {}
    for i in range(7):  # 0 for "Open", 1-6 for strings
        text = "Open" if i == 0 else str(i)
        button = tk.Button(button_frame, text=text, command=lambda i=i: on_button_click(i, button_widgets))
        button.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        button_widgets[i] = button
    
    state_vars["button_widgets"] = button_widgets

    # Duration input
    tk.Label(button_frame, text="Duration (seconds):").grid(row=1, column=0, columnspan=2, pady=5, sticky="w")
    duration_var = tk.StringVar()
    duration_entry = tk.Entry(button_frame, textvariable=duration_var)
    duration_entry.grid(row=1, column=2, columnspan=3, pady=5, padx=5, sticky="w")

    submit_button = tk.Button(button_frame, text="Submit", command=lambda: submit_data())
    submit_button.grid(row=1, column=5, columnspan=2, pady=5, padx=5, sticky="w")

    def submit_data():
        """
        Submit the current state, string number, and duration to the server.
        
        This function validates the input, sends data to the server, 
        updates the status display, and invokes the callback function.
        """
        if state_vars["state"] == "random":
            messagebox.showinfo("Random Mode Active", "Inputs not accepted while in Random Mode. Exit Random Mode to continue.")
            return
        on_duration_submit(duration_var)
        if state_vars["state"] == "get_angles":
            # Send data to the server
            send_data_to_server(state_vars["state"], state_vars["string_num"], state_vars["duration"])
            # Fetch and update status from server
            status_message = fetch_message_from_server(state_vars["string_num"], state_vars["duration"])
            update_status(status_message)
            # Invoke the callback with the current state, string number, and duration
            on_data_submit(state_vars["state"], state_vars["string_num"], state_vars["duration"])

    def toggle_random_mode():
        """
        Toggle between random and manual control modes.
        
        In random mode, all user inputs are disabled, and the button appearance changes.
        In manual mode, all user inputs are enabled, and button states are reset.
        """
        if state_vars["state"] == "ready":
            # Entering random mode
            state_vars["state"] = "random"
            random_mode_button.config(
                relief=tk.SUNKEN, 
                text="Random Mode (ON)", 
                bg="#990000", 
                fg="white", 
                font=("Helvetica", 10, "bold"),
                activebackground="#990000",
                activeforeground="white"
            )
            # Disable all input widgets
            for button in button_widgets.values():
                button.config(state=tk.DISABLED)
            duration_entry.config(state=tk.DISABLED)
            submit_button.config(state=tk.DISABLED)
            
        elif state_vars["state"] == "random":
            # Exiting random mode
            state_vars["state"] = "ready"
            random_mode_button.config(
                relief=tk.RAISED, 
                text="Random Mode (OFF)", 
                bg="#f0f0f0",
                fg="black", 
                font=("Helvetica", 10, "normal"),
                activebackground="#f0f0f0",
                activeforeground="black"
            )
            # Enable all input widgets
            for button in button_widgets.values():
                button.config(state=tk.NORMAL)
            duration_entry.config(state=tk.NORMAL)
            submit_button.config(state=tk.NORMAL)
            
            # Reset any active button states
            if state_vars["active_button"]:
                state_vars["active_button"].config(relief=tk.RAISED)
                state_vars["active_button"] = None
            state_vars["selected_button"] = None

    random_mode_button = tk.Button(
        controls_frame,
        text="Random Mode (OFF)",
        relief=tk.RAISED,
        command=toggle_random_mode
    )
    random_mode_button.pack(side=tk.TOP, pady=10, anchor="w")

    # Status section
    status_frame = tk.Frame(controls_frame, padx=10, pady=10)
    status_frame.pack(side=tk.TOP, fill=tk.X, pady=10, anchor="w")

    status_text = tk.StringVar()
    status_text.set("Status: Idle")
    status_label = tk.Label(status_frame, textvariable=status_text, font=("Helvetica", 12))
    status_label.pack(anchor="w")

    # Bind the Enter key and the 10-key Enter key to the submit_data function
    root.bind("<Return>", lambda event: submit_data())
    root.bind("<KP_Enter>", lambda event: submit_data())

    # Exit button
    tk.Button(root, text="Exit", command=on_exit_click).place(relx=0.02, rely=0.95, anchor="sw")

    root.mainloop()
    
if __name__ == "__main__":
    def dummy_on_data_submit(state, string_num, duration):
        """
        Example callback function for handling submitted data.
        
        Args:
            state (str): Current state of the application
            string_num (int): Selected string number (0-6)
            duration (float): Duration in seconds
        """
        print(f"Data submitted: state={state}, string_num={string_num}, duration={duration}")

    gui_launch(random_flag=False, on_data_submit=dummy_on_data_submit)