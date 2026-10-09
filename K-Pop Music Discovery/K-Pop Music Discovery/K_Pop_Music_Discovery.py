import sqlite3
import tkinter as tk

def init_db():
    # Connect to the SQLite database
    conn = sqlite3.connect("kpop_music.db")
    cursor = conn.cursor()


    cursor.execute()
    conn.commit()
    return conn

def main():
    # Create the main window
    root = tk.Tk()
    root.title("K-Pop Music Discovery")
    root.geometry("400x300")

    # Create a label
    label = tk.Label(root, text="Welcome to K-Pop Music Discovery!", font=("Helvetica", 16))
    label.pack(pady=20)

    # Create a button to discover music
    discover_button = tk.Button(root, text="Discover Music", command=discover_music)
    discover_button.pack(pady=10)

    # Start the main event loop
    root.mainloop()