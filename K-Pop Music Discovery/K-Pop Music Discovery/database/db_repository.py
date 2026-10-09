import sqlite3
from pathlib import Path

DATABASE_NAME = Path(__file__).resolve().parent / "kpop_discovery.db"

class DatabaseRepository:

    def __init__(self):
        self.database_name = DATABASE_NAME

    def initialize_database(self):
        connection = sqlite3.connect(self.database_name)
        
        # TEMP: This is new for me but from what I am researching this enforces foreign key constraints in SQLite.
        connection.execute("PRAGMA foreign_keys = ON;")

        # TEMP: Create a song table if it doesn't exist
        connection.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                song_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                artist TEXT NOT NULL
            );
        """)

        # TEMP: Create a ratings table and associate it with song ID
        connection.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                rating_id INTEGER PRIMARY KEY,
                song_id INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                FOREIGN KEY (song_id) REFERENCES songs (song_id)
            );
        """)
        
        connection.close()
        