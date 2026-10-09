# Create the main application window and all logic pertaining to the UI

import tkinter as tk
from tkinter import ttk

# Window presets
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "K-Pop Music Discovery"

# Creating the main application window class
class AppWindow(tk.Tk):
    def __init__(self):
        # TEMP: This is calling the base class constructor to initialize the Tkinter window.  Similar to C++
        super().__init__()
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.search_var = tk.StringVar()

        # TEMP: This is essentially calling a function which is defined below.  This is a common pattern in Python to keep the constructor clean and organized.
        self._create_widgets()
        self._layout_widgets()

    def _create_widgets(self):
