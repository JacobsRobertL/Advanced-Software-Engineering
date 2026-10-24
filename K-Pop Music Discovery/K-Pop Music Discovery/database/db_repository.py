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

        # TEMP: This is a cleanup method that will run every time.  While it is not needed repeatedly this wont cause any significant perfomance issue
        connection.execute("""
            DELETE FROM preferences
            WHERE preference_id NOT IN (
                SELECT MIN(preference_id)
                FROM preferences
                GROUP BY preference_type COLLATE NOCASE, preference_value COLLATE NOCASE
            )
        """)

        connection.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_preferences_unique_nocase
            ON preferences (preference_type COLLATE NOCASE, preference_value COLLATE NOCASE)
        """)



        connection.execute("""
            CREATE TABLE IF NOT EXISTS recommendations (
                recommendation_id INTEGER PRIMARY KEY,
                song_id INTEGER NOT NULL,
                recommended_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (song_id) REFERENCES songs (song_id)
            );
        """)
        
        connection.commit()
        connection.close()
        
    def add_preference(self, preference_type, preference_value):
        connection = sqlite3.connect(self.database_name)

        connection.execute("""
                INSERT OR IGNORE INTO preferences (preference_type, preference_value)
                VALUES (?, ?)
            """, (preference_type, preference_value))
        
        connection.commit()
        connection.close()

    def has_equivalent_tag(self, tag_value):
        from services.recommendation_service import normalize_tag

        normalized_value = normalize_tag(tag_value)

        for preference_type, preference_value in self.get_preferences():
            if preference_type.strip().casefold() == "tag":
                if normalize_tag(preference_value) == normalized_value:
                    return True

        return False

    def get_preferences(self):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT preference_type, preference_value FROM preferences ORDER BY preference_type, preference_value")
        preferences = cursor.fetchall()
        connection.close()
        return preferences

    def save_recommendation(self, title, artist):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()

        # Check if the song already exists in the songs table
        cursor.execute("SELECT song_id FROM songs WHERE title = ? AND artist = ?", (title, artist))
        song = cursor.fetchone()
        if song:
            song_id = song[0]
        else:
            # Insert the new song into the songs table
            cursor.execute("INSERT INTO songs (title, artist) VALUES (?, ?)", (title, artist))
            song_id = cursor.lastrowid
        # Insert the recommendation into the recommendations table
        cursor.execute("INSERT INTO recommendations (song_id) VALUES (?)", (song_id,))
        
        connection.commit()
        connection.close()

    def save_rating(self, title, artist, rating):
        if not isinstance(rating, int) or isinstance(rating, bool) or not 1 <= rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5.")

        connection = sqlite3.connect(self.database_name)
        connection.execute("PRAGMA foreign_keys = ON;")

        try:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT song_id FROM songs WHERE title = ? AND artist = ?",
                (title, artist)
            )
            song = cursor.fetchone()

            if song is None:
                raise ValueError("Song must be saved before it can be rated.")

            cursor.execute("""
                INSERT INTO ratings (song_id, rating)
                VALUES (?, ?)
                ON CONFLICT(song_id) DO UPDATE SET rating = excluded.rating
            """, (song[0], rating))

            connection.commit()
        finally:
            connection.close()

    def get_song_rating(self, title, artist):
        connection = sqlite3.connect(self.database_name)

        try:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT ratings.rating
                FROM ratings
                JOIN songs ON ratings.song_id = songs.song_id
                WHERE songs.title = ? AND songs.artist = ?
            """, (title, artist))

            result = cursor.fetchone()

            return result[0] if result else None
        finally:
            connection.close()

    def get_rated_songs(self):
        connection = sqlite3.connect(self.database_name)

        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT songs.title, songs.artist, ratings.rating
                FROM ratings
                JOIN songs ON ratings.song_id = songs.song_id
                ORDER BY songs.artist, songs.title
            """)
            return cursor.fetchall()
        finally:
            connection.close()

    def get_artist_rating_adjustments(self):
        rated_songs = self.get_rated_songs()
        artist_ratings = {}

        for title, artist, rating in rated_songs:
            artist_key = artist.strip().casefold()
            artist_ratings.setdefault(artist_key, []).append(rating)

        adjustments = {}

        for artist, ratings in artist_ratings.items():
            average_rating = sum(ratings) / len(ratings)
            adjustments[artist] = round((average_rating - 3) * 1)

        return adjustments

    def get_recommendation_history(self):
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute("""
            SELECT 
                songs.title, 
                songs.artist, 
                recommendations.recommended_at
            FROM recommendations
            JOIN songs 
                ON recommendations.song_id = songs.song_id
            ORDER BY recommendations.recommendation_id DESC
        """)
        history = cursor.fetchall()
        connection.close()
        return history

    def clear_recommendation_history(self):
        connection = sqlite3.connect(self.database_name)

        connection.execute("DELETE FROM recommendations")
        connection.commit()
        connection.close()

    def clear_preferences(self):
        connection = sqlite3.connect(self.database_name)

        connection.execute("DELETE FROM preferences")
        connection.commit()
        connection.close()

if __name__ == "__main__":
    db = DatabaseRepository()

    history = db.get_recommendation_history()

    for title, artist, recommended_at in history:
        print(f"{recommended_at} | {artist} - {title}")