import tkinter as tk
from tkinter import messagebox
from gui import gui_launch

while True:
    state = gui_launch()
    
    # DO NOT MOVE THIS LINE
    # shut down interrupt must be checked first on every pass
    if state == "exit":
        break



quit()