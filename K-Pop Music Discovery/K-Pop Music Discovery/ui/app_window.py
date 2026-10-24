# Create the main application window and all logic pertaining to the UI

import tkinter as tk
from tkinter import ttk, messagebox

from api.lastfm_client import (
    get_top_tracks,
    get_song_tags,
    search_artists,
    search_tracks,
    get_similar_artists
    )

from services.recommendation_service import (
    generate_recommendations,
    save_generated_recommendations,
    remove_duplicate_recommendations,
    remove_previously_recommended,
    remove_unusable_tracks,
    filter_by_artist,
    add_track_tags,
    filter_by_tag,
    parse_artist_search_results,
    parse_track_search_results,
    get_selectable_song_tags,
    generate_discovery_recommendations,
    score_recommendations,
    enrich_recommendations
    )

from adapters.musicbrainz_adapter import MusicBrainzAdapter

# Window presets
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_TITLE = "K-Pop Music Discovery"

# Creating the main application window class
class AppWindow(tk.Tk):
    def __init__(self, db_repo):
        
        # TEMP: This is calling the base class constructor to initialize the Tkinter window.  Similar to C++
        super().__init__()
        self.configure(background="#F0F0F0")


        self.db_repo = db_repo


        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(False, False)

        self.search_var = tk.StringVar()
        self.search_in_progress = False

        # TEMP: This is essentially calling a function which is defined below.  This is a common pattern in Python to keep the constructor clean and organized.
        self._configure_styles()
        self._create_widgets()
        self._layout_widgets()

        # TEMP: Test loading profile from the database
        self.preference_profile = self._load_preference_profile()
        self._display_preferences()
        print("Initial preference profile:", self.preference_profile)

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background="#F0F0F0")
        style.configure("TLabel", background="#F0F0F0", foreground="#111827")
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), foreground="white", background="#2563EB", bordercolor="#1D4ED8", lightcolor="#2563EB", darkcolor="#1D4ED8", borderwidth=2, relief="raised", padding=(12, 6))
        style.map("Action.TButton", background=[("disabled", "#CBD5E1"), ("pressed", "#1E40AF"), ("active", "#1D4ED8")], foreground=[("disabled", "#64748B"), ("active", "white")], bordercolor=[("pressed", "#1E3A8A"), ("active", "#1E40AF")], relief=[("pressed", "sunken"), ("!pressed", "raised")])
        style.configure("Discover.TButton", font=("Segoe UI", 11, "bold"), foreground="white", background="#7C3AED", bordercolor="#5B21B6", lightcolor="#7C3AED", darkcolor="#5B21B6", borderwidth=2, relief="raised", padding=(24, 10))
        style.map("Discover.TButton", background=[("disabled", "#CBD5E1"), ("pressed", "#5B21B6"), ("active", "#6D28D9")], foreground=[("disabled", "#64748B"), ("active", "white")], bordercolor=[("pressed", "#4C1D95"), ("active", "#5B21B6")], relief=[("pressed", "sunken"), ("!pressed", "raised")])
        style.configure("Clear.TButton", font=("Segoe UI", 9), foreground="#9F3030", background="#FCE8E8", padding=(10,5), borderwidth=1, relief="flat")
        style.map("Clear.TButton", background=[("pressed", "#F5BABA"), ("active", "#F8D5D5")], foreground=[("disabled", "#999999")])

    # TEMP: This only creates the widgets but does not place them.
    def _create_widgets(self):
        self.title_label = ttk.Label(self, text="K-Pop Music Discovery", font=("Helvetica", 22))
        self.preference_header_frame = ttk.Frame(self)
        self.discovery_header_frame = ttk.Frame(self)
        
        self.search_label = ttk.Label(self, text="1. Search Music:", font=("Segoe UI", 11, "bold"))
        self.search_frame = ttk.Frame(self)
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self._on_search, style="Action.TButton")
        self.search_entry.bind("<Return>", lambda event: self._on_search())
        
        # Search result containers
        self.results_frame = ttk.Frame(self)

        # Artist results
        self.artist_results_frame = ttk.Frame(self.results_frame)
        self.artist_results_label = ttk.Label(self.artist_results_frame, text="Artists:", font=("Segoe UI", 10, "bold"))
        self.artist_results_listbox = tk.Listbox(self.artist_results_frame, height=5, exportselection=False)
        self.artist_results_scrollbar = ttk.Scrollbar(self.artist_results_frame, orient="vertical", command=self.artist_results_listbox.yview)
        self.artist_results_listbox.configure(yscrollcommand=self.artist_results_scrollbar.set)
        self.artist_results_listbox.bind("<<ListboxSelect>>", self._on_artist_selected)

        # Song results
        self.track_results_frame = ttk.Frame(self.results_frame)
        self.track_results_label = ttk.Label(self.track_results_frame, text="Songs:", font=("Segoe UI", 10, "bold"))
        self.track_results_listbox = tk.Listbox(self.track_results_frame, height=5, exportselection=False)
        self.track_results_scrollbar = ttk.Scrollbar(self.track_results_frame, orient="vertical", command=self.track_results_listbox.yview)
        self.track_results_listbox.configure(yscrollcommand=self.track_results_scrollbar.set)
        self.track_results_listbox.bind("<<ListboxSelect>>", self._on_track_selected)
        self.search_actions_frame = ttk.Frame(self.results_frame)
        self.add_selected_button = ttk.Button(self.search_actions_frame, text="Add Selected to Preferences", style="Action.TButton", command=self._on_add_selected_preference)
        self.view_tags_button = ttk.Button(self.search_actions_frame, text="View Song Tags", style="Action.TButton", command=self._on_view_song_tags)
       
        self.discovery_label = ttk.Label(self.discovery_header_frame, text="3. Discover Music:", font=("Segoe UI", 11, "bold"))
        self.discovery_frame = ttk.Frame(self)
        self.discovery_listbox = tk.Listbox(self.discovery_frame, height = 5)
        self.discovery_scrollbar = ttk.Scrollbar(self.discovery_frame, orient="vertical", command=self.discovery_listbox.yview)
        self.discovery_listbox.configure(yscrollcommand=self.discovery_scrollbar.set)

        self.clear_history_button = ttk.Button(self.discovery_header_frame, text="Clear Recommendation History", command=self._on_clear_history, style="Clear.TButton")
        self.clear_preferences_button = ttk.Button(self.preference_header_frame, text="Clear Preference Profile", command=self._on_clear_preferences, style="Clear.TButton")

        self.discover_button = ttk.Button(self, text="Discover Music", command=self._on_discover, style="Discover.TButton")

    # TEMP: Adding preference widgets
        self.preference_input_frame = ttk.Frame(self)
        self.preference_var = tk.StringVar()
        self.preference_type_var = tk.StringVar(value="Artist")
        self.preference_label = ttk.Label(self.preference_header_frame, text="2. Your Preferences:", font=("Segoe UI", 11, "bold"))
        self.preference_type_dropdown = ttk.Combobox(self.preference_input_frame, textvariable=self.preference_type_var, values=["Artist", "Tag"], state="readonly", width = 12)
        self.preference_entry = ttk.Entry(self.preference_input_frame, textvariable=self.preference_var)
        self.preference_placeholder = "Enter artist or tag"
        self.preference_var.set(self.preference_placeholder)
        self.preference_entry.bind("<FocusIn>", self._on_preference_focus_in)
        self.preference_entry.bind("<FocusOut>", self._on_preference_focus_out)

        self.add_preference_button = ttk.Button(self.preference_input_frame, text="Add Preference", command=self._on_add_preference, style="Action.TButton")
        self.preference_frame = ttk.Frame(self)

        self.preference_listbox = tk.Listbox(self.preference_frame, height=5)  
        self.preference_scrollbar = ttk.Scrollbar(self.preference_frame, orient="vertical", command=self.preference_listbox.yview)
        self.preference_listbox.configure(yscrollcommand=self.preference_scrollbar.set)

        self.search_separator = ttk.Separator(self, orient="horizontal")
        self.preferences_separator = ttk.Separator(self, orient="horizontal")
        self.title_separator = ttk.Separator(self, orient="horizontal")

    def _on_preference_focus_in(self, event):
        if self.preference_var.get() == self.preference_placeholder:
            self.preference_var.set("")


    def _on_preference_focus_out(self, event):
        if not self.preference_var.get().strip():
            self.preference_var.set(self.preference_placeholder)

    # TEMP: This places the widgets
    def _layout_widgets(self):
        # App title
        self.title_label.pack(pady=(15,12))
        self.title_separator.pack(fill="x", padx=100, pady=(0,15))
        
        # Search Section
        self.search_label.pack(anchor="w", padx=20, pady=(10, 5))
        self.search_frame.pack(padx=20, pady=5, fill="x")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.search_button.pack(side="right")
        self.results_frame.pack(fill="x", padx=20, pady=(8, 0))
        self.search_actions_frame.pack(side="bottom", pady=(10, 0))
        self.add_selected_button.pack(side="left", padx=(0, 8))
        self.view_tags_button.pack(side="left")

        self.artist_results_frame.pack(side="left", fill="both", expand=True, padx=(0, 6))
        self.track_results_frame.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.artist_results_label.pack(anchor="w", pady=(0, 4))
        self.track_results_label.pack(anchor="w", pady=(0, 4))

        self.artist_results_scrollbar.pack(side="right", fill="y")
        self.artist_results_listbox.pack(side="left", fill="both", expand=True)

        self.track_results_scrollbar.pack(side="right", fill="y")
        self.track_results_listbox.pack(side="left", fill="both", expand=True)

        # Separator
        self.search_separator.pack(padx=20, pady=(18,18), fill="x")

        # Preferences section
        self.preference_header_frame.pack(padx=20, pady=(5,5), fill="x")
        self.preference_label.pack(side="left")
        self.clear_preferences_button.pack(side="right")
        
        self.preference_frame.pack(padx=20, pady=(5, 5), fill="x")
        self.preference_listbox.pack(side="left", fill="both", expand=True)
        self.preference_scrollbar.pack(side="right", fill="y")

        self.preference_input_frame.pack(padx=20, pady=(5, 5), fill="x")
        self.preference_type_dropdown.pack(side="left", padx=(0,10))
        self.preference_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.add_preference_button.pack(side="right")

        # Separator
        self.preferences_separator.pack(padx=20, pady=(18,18), fill="x")

        # Discovery section
        self.discovery_header_frame.pack(padx=20, pady=(5,5), fill="x")
        self.discovery_label.pack(side="left")
        self.clear_history_button.pack(side="right")
        self.discover_button.pack(pady=(5,10))

        self.discovery_frame.pack(padx=20, pady=(5, 5), fill="x")
        self.discovery_listbox.pack(side="left", fill="both", expand=True)
        self.discovery_scrollbar.pack(side="right", fill="y")


    # TEMP: This is the function that will be called when the search button is clicked.
    def _on_search(self):
        if self.search_in_progress:
            return

        search_term = self.search_var.get().strip()
        if not search_term:
            return

        self.search_in_progress = True
        self.search_button.configure(state="disabled")

        artist_response = search_artists(search_term)
        track_response = search_tracks(search_term)

        artists = parse_artist_search_results(artist_response)
        tracks = parse_track_search_results(track_response)

        self.artist_search_results = artists
        self.track_search_results = tracks

        self.artist_results_listbox.delete(0, tk.END)
        self.track_results_listbox.delete(0, tk.END)

        for artist in artists:
            self.artist_results_listbox.insert(tk.END, artist["artist"])

        for track in tracks:
            self.track_results_listbox.insert(tk.END, f"{track['title']} — {track['artist']}")

        if not artists:
            self.artist_results_listbox.insert(tk.END, "No artists found.")

        if not tracks:
            self.track_results_listbox.insert(tk.END, "No songs found.")

        self._finish_search()


    def _finish_search(self):
        self.search_in_progress = False
        self.search_button.configure(state="normal")
        self.search_entry.configure(state="normal")

    # TEMP: This displays the results in the listbox.  As we have not contacted the API yet this is a placeholder
    def _display_results(self, results):
        self.results_listbox.delete(0, tk.END)  # Clear previous results
        
        for result in results:
            self.results_listbox.insert(tk.END, result)

    def _display_discoveries(self, recommendations):
        self.discovery_listbox.delete(0, tk.END)

        for recommendation in recommendations:
            self.discovery_listbox.insert(tk.END, recommendation)

    def _on_artist_selected(self, event):
        if self.artist_results_listbox.curselection():
            self.track_results_listbox.selection_clear(0, tk.END)

    def _on_track_selected(self, event):
        if self.track_results_listbox.curselection():
            self.artist_results_listbox.selection_clear(0, tk.END)


    # TEMP callback for adding preferences
    def _on_add_preference(self):
        preference = self.preference_var.get().strip()
        if not preference or preference == self.preference_placeholder:
            return  # TEMP: Do nothing if the preference is empty
        
        preference_type = self.preference_type_var.get()

        if preference_type.strip().casefold() == "tag" and self.db_repo.has_equivalent_tag(preference):
            messagebox.showinfo("Duplicate Tag", f"An equivalent tag preference already exists: {preference}")
            return

        self.db_repo.add_preference(preference_type.strip().lower(), preference)

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
        print("Raw database preferences:", self.db_repo.get_preferences())
        preferences = self.db_repo.get_preferences()
        self.preference_listbox.delete(0, tk.END)  # Clear previous preferences

        profile = {"artists": [], "tags": []}
        
        for preference_type, preference_value in preferences:
            preference_type = preference_type.strip().lower()
            self.preference_listbox.insert(tk.END, f"{preference_type.title()}: {preference_value}")

            if preference_type == "artist":  # TEMP: Assuming we only care about artist preferences for now
                profile["artists"].append(preference_value)
            elif preference_type == "tag":  # TEMP: Assuming we only care about tag preferences for now
                profile["tags"].append(preference_value)

        return profile

    def _on_clear_history(self):
        confirmed = messagebox.askyesno("Clear Recommendation History", "Are you sure you want to clear the recommendation history?\n\nThis action cannot be undone.") 
        if confirmed:
            self.db_repo.clear_recommendation_history()
            self._display_discoveries([])
            messagebox.showinfo("History Cleared", "Recommendation history has been cleared.")

    def _on_clear_preferences(self):
        confirmed = messagebox.askyesno("Clear Preference Profile", "Are you sure you want to clear Your preference profile?\n\nThis action cannot be undone.") 
        if confirmed:
            self.db_repo.clear_preferences()
            self.preference_profile = self._load_preference_profile()
            self._display_preferences()
            messagebox.showinfo("Preferences Cleared", "Preference profile has been cleared.")

    def _on_discover(self):
        self.preference_profile = self._load_preference_profile()
        print("DATABASE PREFERENCES:", self.db_repo.get_preferences())
        print("LOADED PROFILE:", self.preference_profile)

        preferred_artists = self.preference_profile["artists"]
        preferred_tags = self.preference_profile["tags"]

        if not preferred_artists:
            messagebox.showinfo(
                "No Artist Preferences",
                "Please add at least one artist preference before discovering music."
            )
            return

        recommendations = generate_discovery_recommendations(preferred_artists, get_similar_artists, get_top_tracks)
        recommendations = remove_unusable_tracks(recommendations)
        recommendations = remove_duplicate_recommendations(recommendations)

        history = self.db_repo.get_recommendation_history()
        recommendations = remove_previously_recommended(recommendations, history)
        
        if preferred_tags and recommendations:
            recommendations = add_track_tags(recommendations, get_song_tags)

        recommendations = score_recommendations(recommendations, preferred_tags)

        adapter = MusicBrainzAdapter()
        recommendations = enrich_recommendations(recommendations, adapter, limit=3)

        save_generated_recommendations(recommendations, self.db_repo.save_recommendation)
        
        display_results = []

        for track in recommendations:
            recording_id = track.get("musicbrainz_id", "Not matched")
            display_results.append(f"{track['title']} — {track['artist']} (Score: {track['score']}, MBID: {recording_id})")

        self._display_discoveries(display_results)
        print("PREFERENCES LISTBOX AFTER DISCOVER:", self.preference_listbox.get(0, tk.END))

    def _on_add_selected_preference(self):
        artist_selection = self.artist_results_listbox.curselection()
        track_selection = self.track_results_listbox.curselection()

        if artist_selection:
            index = artist_selection[0]
            artist_name = self.artist_search_results[index]["artist"]

        elif track_selection:
            index = track_selection[0]
            artist_name = self.track_search_results[index]["artist"]

        else:
            messagebox.showinfo("No Selection", "Please select an artist or song first.")
            return

        self.db_repo.add_preference("artist", artist_name)

        self.preference_profile = self._load_preference_profile()
        self._display_preferences()

        messagebox.showinfo("Preference Added", f"Added {artist_name} to your preferences.")

    def _on_view_song_tags(self):
        selection = self.track_results_listbox.curselection()

        if not selection:
            messagebox.showinfo("No Song Selected", "Please select a song first.")
            return

        index = selection[0]
        track = self.track_search_results[index]

        popup = tk.Toplevel(self)
        popup.title("Song Tags")
        popup.geometry("420x350")
        popup.resizable(False, False)
        popup.configure(background="#F7F8FC")

        style = ttk.Style(popup)
        style.configure("Tag.TCheckbutton", background="#F7F8FC", foreground="#27334D", font=("Segoe UI", 10), padding=(6, 4))
        style.map("Tag.TCheckbutton", background=[("active", "#F7F8FC"), ("selected", "#F7F8FC")])
        style.configure("Tags.TFrame", background="#F7F8FC")

        ttk.Label(popup, text=track["title"], font=("Segoe UI", 15, "bold"), background="#F7F8FC", foreground="#20263B").pack(pady=(20, 2))
        ttk.Label(popup, text=track["artist"], font=("Segoe UI", 10), background="#F7F8FC", foreground="#65718A").pack(pady=(0, 12))
        
        response = get_song_tags(track["artist"], track["title"])
        tags = get_selectable_song_tags(response)

        tag_selections = []

        if tags:
            tags_frame = ttk.Frame(popup, style="Tags.TFrame")
            tags_frame.pack(pady=(5, 10))

            for index, tag in enumerate(tags):
                selected = tk.BooleanVar(master=popup, value=False)

                checkbox = ttk.Checkbutton(tags_frame, text=tag, variable=selected, style="Tag.TCheckbutton")
                checkbox.grid(row=index // 2, column=index % 2, sticky="w", padx=15, pady=3)

                tag_selections.append((tag, selected))
        else:
            ttk.Label(popup, text="No tags available for this song").pack(pady=10)

        def save_selected_tags():
            selected_tags = [tag for tag, selected in tag_selections if selected.get()]

            if not selected_tags:
                messagebox.showinfo("No Tags Selected", "Please select at least one tag.", parent=popup)
                return

            for tag in selected_tags:
                if not self.db_repo.has_equivalent_tag(tag):
                    self.db_repo.add_preference("tag", tag)

            self.preference_profile = self._load_preference_profile()
            self._display_preferences()
            popup.destroy()

        buttons_frame = ttk.Frame(popup, style="Tags.TFrame")
        buttons_frame.pack(pady=(15, 10))

        ttk.Button(buttons_frame, text="Cancel", command=popup.destroy).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Add Selected Tags", style="Action.TButton", command=save_selected_tags).pack(side="left", padx=5)