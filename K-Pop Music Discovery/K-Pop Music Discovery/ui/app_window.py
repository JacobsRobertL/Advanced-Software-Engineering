# Create the main application window and all logic pertaining to the UI

import tkinter as tk
from tkinter import ttk, messagebox

from api.lastfm_client import (
    get_top_tracks,
    get_song_tags,
    )

from services.recommendation_service import (
    generate_recommendations,
    save_generated_recommendations,
    remove_duplicate_recommendations,
    remove_previously_recommended,
    filter_by_artist,
    add_track_tags,
    filter_by_tag,
    )

# Window presets
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 750
WINDOW_TITLE = "K-Pop Music Discovery"

# Creating the main application window class
class AppWindow(tk.Tk):
    def __init__(self, db_repo):
        
        # TEMP: This is calling the base class constructor to initialize the Tkinter window.  Similar to C++
        super().__init__()


        self.db_repo = db_repo


        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.search_var = tk.StringVar()
        self.search_in_progress = False

        # TEMP: This is essentially calling a function which is defined below.  This is a common pattern in Python to keep the constructor clean and organized.
        self._create_widgets()
        self._layout_widgets()

        # TEMP: Test loading profile from the database
        self.preference_profile = self._load_preference_profile()
        self._display_preferences()
        print("Initial preference profile:", self.preference_profile)

    # TEMP: This only creates the widgets but does not place them.
    def _create_widgets(self):
        self.title_label = ttk.Label(self, text="K-Pop Music Discovery", font=("Helvetica", 24))
        
        self.search_label = ttk.Label(self, text="Let's start with songs you like:")
        self.search_frame = ttk.Frame(self)
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self._on_search)
        self.search_entry.bind("<Return>", lambda event: self._on_search())
        
        self.results_label = ttk.Label(self, text="Results:")
        self.results_frame = ttk.Frame(self)
        self.results_listbox = tk.Listbox(self.results_frame, height=8)
        self.results_scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_listbox.yview)
        self.results_listbox.configure(yscrollcommand=self.results_scrollbar.set)
        
        self.clear_history_button = ttk.Button(self, text="Clear Recommendation History", command=self._on_clear_history)
        self.clear_preferences_button = ttk.Button(self, text="Clear Preference Profile", command=self._on_clear_preferences)

    # TEMP: Adding preference widgets
        self.preference_var = tk.StringVar()
        self.preference_type_var = tk.StringVar(value="artist")
        self.preference_label = ttk.Label(self, text="Add a favorite artist or tag:")
        self.preference_type_dropdown = ttk.Combobox(self, textvariable=self.preference_type_var, values=["artist", "tag"], state="readonly", width = 12)
        self.preference_entry = ttk.Entry(self, textvariable=self.preference_var)
        self.preference_placeholder = "Enter artist or tag"
        self.preference_var.set(self.preference_placeholder)
        self.preference_entry.bind("<FocusIn>", self._on_preference_focus_in)
        self.preference_entry.bind("<FocusOut>", self._on_preference_focus_out)

        self.add_preference_button = ttk.Button(self, text="Add Preference", command=self._on_add_preference)
        self.preference_frame = ttk.Frame(self)

        self.preference_listbox = tk.Listbox(self.preference_frame, height=8)  
        self.preference_scrollbar = ttk.Scrollbar(self.preference_frame, orient="vertical", command=self.preference_listbox.yview)
        self.preference_listbox.configure(yscrollcommand=self.preference_scrollbar.set)

    def _on_preference_focus_in(self, event):
        if self.preference_var.get() == self.preference_placeholder:
            self.preference_var.set("")


    def _on_preference_focus_out(self, event):
        if not self.preference_var.get().strip():
            self.preference_var.set(self.preference_placeholder)

    # TEMP: This places the widgets
    def _layout_widgets(self):
        self.title_label.pack(pady=20)
        
        self.search_label.pack(pady=10)
        self.search_frame.pack(padx=20, pady=5, fill="x")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.search_button.pack(side="right")
        
        self.results_label.pack(pady=10)
        self.results_frame.pack(padx=20, pady=10, fill="x")

        self.results_listbox.pack(side="left", fill="both", expand=True)
        self.results_scrollbar.pack(side="right", fill="y")

        # TEMP: Adding preference widgets to the layout
        self.clear_history_button.pack(pady=10)
        self.preference_label.pack(pady=(10, 0))
        self.preference_type_dropdown.pack(pady=5)
        self.preference_entry.pack(padx = 20, pady=5, fill=tk.X)

        self.add_preference_button.pack(pady=10)
        self.preference_frame.pack(padx=20, pady=(10,30), fill="x")
        self.preference_listbox.pack(side="left", fill="both", expand=True)
        self.preference_scrollbar.pack(side="right", fill="y")
        self.clear_preferences_button.pack(pady=(5,20))

    # TEMP: This is the function that will be called when the search button is clicked.
    def _on_search(self):

        if self.search_in_progress:
            return

        search_term = self.search_var.get().strip()
        if not search_term:
            return

        self.search_in_progress = True
        self.search_button.configure(state="disabled")

        # TEMP: Grab the term from the box and strip whitespace
        search_term = self.search_var.get().strip()
        if not search_term:
            return  # TEMP: Do nothing if the search term is empty

        # Generate recommendations using Last.fm
        recommendations = generate_recommendations(
                [search_term],
                get_top_tracks
            )
        print("After generating recommendations:", len(recommendations))

        recommendations = filter_by_artist(recommendations, [search_term])
        # TEMP: print("After artist filtering:", len(recommendations))

        recommendations = remove_duplicate_recommendations(recommendations)
        #TEMP: print("After duplicate removal:", len(recommendations))

        history = self.db_repo.get_recommendation_history()
        #TEMP: print("History count:", len(history))

        recommendations = remove_previously_recommended(recommendations, history)
        #TEMP: print("After history filtering:", len(recommendations))

        recommendations = add_track_tags(recommendations, get_song_tags)

        preferred_tags = self.preference_profile["tags"]

        if preferred_tags:
            recommendations = filter_by_tag(recommendations, preferred_tags)

        print("After tag filtering:", len(recommendations))

        # TEMP: Temporarily print the recommendations to the console for debugging
        for track in recommendations:
            print(f"Recommended: {track['artist']} - {track['title']}")
            print(f"Tags: {track['tags']}")

        # Save the recommendations to SQLite
        save_generated_recommendations(
                recommendations,
                self.db_repo.save_recommendation
            )

        # Display recommendations in Tkinter
        results = []

        for track in recommendations:
            results.append(f"{track['artist']} - {track['title']}")

        if not results:
            results.append("No new recommendations available.")

        self._display_results(results)

        print(f"New recommendations saved: {len(recommendations)}")

        self.after(300, self._finish_search)

    def _finish_search(self):
        self.search_in_progress = False
        self.search_button.configure(state="normal")
        self.search_entry.configure(state="normal")

    # TEMP: This displays the results in the listbox.  As we have not contacted the API yet this is a placeholder
    def _display_results(self, results):
        self.results_listbox.delete(0, tk.END)  # Clear previous results
        
        for result in results:
            self.results_listbox.insert(tk.END, result)

    # TEMP callback for adding preferences
    def _on_add_preference(self):
        preference = self.preference_var.get().strip()
        if not preference or preference == self.preference_placeholder:
            return  # TEMP: Do nothing if the preference is empty
        
        preference_type = self.preference_type_var.get()

        self.db_repo.add_preference(preference_type, preference)

        print(f"Preference added: {preference}")  # TEMP: Placeholder for actual functionality

        self.preference_var.set(self.preference_placeholder)  # Clear the entry after adding preference

        self.preference_profile = self._load_preference_profile()  # Reload the preference profile

        self._display_preferences()

        print("Updated preference profile:", self.preference_profile)

    def _display_preferences(self):
        self.preference_listbox.delete(0, tk.END)

        for preference_type, preference_value in self.db_repo.get_preferences():
            self.preference_listbox.insert(tk.END, f"{preference_type.title()}: {preference_value}")


    def _load_preference_profile(self):
        preferences = self.db_repo.get_preferences()
        self.preference_listbox.delete(0, tk.END)  # Clear previous preferences

        profile = {"artists": [], "tags": []}
        
        for preference_type, preference_value in preferences:
            if preference_type == "artist":  # TEMP: Assuming we only care about artist preferences for now
                profile["artists"].append(preference_value)
            elif preference_type == "tag":  # TEMP: Assuming we only care about tag preferences for now
                profile["tags"].append(preference_value)

        return profile

    def _on_clear_history(self):
        confirmed = messagebox.askyesno("Clear Recommendation History", "Are you sure you want to clear the recommendation history?\n\nThis action cannot be undone.") 
        if confirmed:
            self.db_repo.clear_recommendation_history()
            self._display_results([])
            messagebox.showinfo("History Cleared", "Recommendation history has been cleared.")

    def _on_clear_preferences(self):
        confirmed = messagebox.askyesno("Clear Preference Profile", "Are you sure you want to clear Your preference profile?\n\nThis action cannot be undone.") 
        if confirmed:
            self.db_repo.clear_preferences()
            self.preference_profile = self._load_preference_profile()
            self._display_preferences()
            messagebox.showinfo("Preferences Cleared", "Preference profile has been cleared.")