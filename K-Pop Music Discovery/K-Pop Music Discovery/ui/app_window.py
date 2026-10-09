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

    # TEMP: This only creates the widgets but does not place them.
    def _create_widgets(self):
        self.title_label = ttk.Label(self, text="K-Pop Music Discovery", font=("Helvetica", 24))
        
        self.search_label = ttk.Label(self, text="Let's start with songs you like:")
        self.search_entry = ttk.Entry(self, textvariable=self.search_var)
        self.search_button = ttk.Button(self, text="Search", command=self._on_search)
        
        self.results_label = ttk.Label(self, text="Results:")
        self.results_listbox = tk.Listbox(self, height=20, width=80)

    # TEMP: This places the widgets
    def _layout_widgets(self):
        self.title_label.pack(pady=20)
        
        self.search_label.pack(pady=10)
        self.search_entry.pack(pady=5)
        self.search_button.pack(pady=10)
        
        self.results_label.pack(pady=10)
        self.results_listbox.pack(pady=5)

    # TEMP: This is the function that will be called when the search button is clicked.
    def _on_search(self):
        # TEMP: Grab the term from the box and strip whitespace
        search_term = self.search_var.get().strip()

        if not search_term:
            return  # TEMP: Do nothing if the search term is empty

        self._display_results([f"Searching for: {search_term}"])

    # TEMP: This displays the results in the listbox.  As we have not contacted the API yet this is a placeholder
    def _display_results(self, results):
        self.results_listbox.delete(0, tk.END)  # Clear previous results
        
        for result in results:
            self.results_listbox.insert(tk.END, result)