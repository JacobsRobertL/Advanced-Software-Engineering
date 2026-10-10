import os
import sqlite3
from pathlib import Path

#DATABASE_NAME = Path(__file__).resolve().parent / "kpop_discovery.db"

# TEMP: This is for submission
APP_DATA = Path(os.getenv("LOCALAPPDATA", Path.home())) / "K-Pop Music Discovery"
APP_DATA.mkdir(parents=True, exist_ok=True)
DATABASE_NAME = APP_DATA / "kpop_discovery.db"

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
        # TEMP: Added a rating check which means that I need to delete the local DBRepo to recreate with new params.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                rating_id INTEGER PRIMARY KEY,
                song_id INTEGER NOT NULL UNIQUE,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                FOREIGN KEY (song_id) REFERENCES songs (song_id)
            );
        """)

        # TEMP: Create a preference table that associates a type with a value.
        connection.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                preference_id INTEGER PRIMARY KEY,
                preference_type TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                UNIQUE (preference_type, preference_value)
            );
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                recommendation_id INTEGER PRIMARY KEY,
                song_id INTEGER NOT NULL,
                recommended_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (song_id) REFERENCES songs (song_id)
            );
        """)
        
        connection.close()
        
    def add_preference(self, preference_type, preference_value):
        connection = sqlite3.connect(self.database_name)

        connection.execute("""
                INSERT OR IGNORE INTO preferences (preference_type, preference_value)
                VALUES (?, ?)
            """, (preference_type, preference_value))
        
        connection.commit()
        connection.close()

    def get_preferences(self):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT preference_type, preference_value FROM preferences ORDER BY preference_type, preference_value")
        preferences = cursor.fetchall()
        connection.close()
        return preferences