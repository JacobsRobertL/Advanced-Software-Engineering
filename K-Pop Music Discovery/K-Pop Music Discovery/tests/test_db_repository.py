from database.db_repository import DatabaseRepository
from services.recommendation_service import save_generated_recommendations

def test_save_recommendation(tmp_path):
    db = DatabaseRepository()

    db.database_name = tmp_path / "test_kpop.db"  # Use a temporary database for testing
    db.initialize_database()  # Initialize the database schema
    
    # Save a recommendation
    db.save_recommendation("Howling", "XG")
    db.save_recommendation("Howling", "XG")
    
    import sqlite3

    # Retrieve the saved recommendation
    connection = sqlite3.connect(db.database_name)

    song_count = connection.execute(
        "SELECT COUNT(*) FROM songs"
    ).fetchone()[0]
    
    recommendation_count = connection.execute(
        "SELECT COUNT(*) FROM recommendations"
    ).fetchone()[0]

    connection.close()
    
    assert song_count == 1
    assert recommendation_count == 2


def test_get_recommendation_history(tmp_path):
    db = DatabaseRepository()

    db.database_name = tmp_path / "test_kpop.db"
    db.initialize_database()

    # Save a recommendation
    db.save_recommendation("Howling", "XG")
    db.save_recommendation("Lemonade", "aespa")

    # Retrieve the recommendation history
    history = db.get_recommendation_history()

    assert len(history) == 2

    assert history[0][0] == "Lemonade"
    assert history[0][1] == "aespa"

    assert history[1][0] == "Howling"
    assert history[1][1] == "XG"


def test_save_generated_recommendations():
    recommendations = [
        {"title": "Howling", "artist": "XG"},
        {"title": "Lemonade", "artist": "aespa"}
    ]

    saved = []

    def test_save(title, artist):
        saved.append((title, artist))

    save_generated_recommendations(recommendations, test_save)

    assert saved == [
        ("Howling", "XG"),
        ("Lemonade", "aespa")
    ]

def test_add_and_get_preferences(tmp_path):
    db = DatabaseRepository()
    db.database_name = tmp_path / "test_kpop.db"
    db.initialize_database()

    db.add_preference("artist", "aespa")
    db.add_preference("tag", "k-pop")

    preferences = db.get_preferences()

    assert ("artist", "aespa") in preferences
    assert ("tag", "k-pop") in preferences
    assert len(preferences) == 2


def test_duplicate_preferences_not_saved(tmp_path):
    db = DatabaseRepository()
    db.database_name = tmp_path / "test_kpop.db"
    db.initialize_database()

    db.add_preference("artist", "aespa")
    db.add_preference("artist", "aespa")

    assert db.get_preferences() == [("artist", "aespa")]


def test_clear_preferences(tmp_path):
    db = DatabaseRepository()
    db.database_name = tmp_path / "test_kpop.db"
    db.initialize_database()

    db.add_preference("artist", "aespa")
    db.add_preference("tag", "k-pop")
    db.save_recommendation("Howling", "XG")

    db.clear_preferences()

    assert db.get_preferences() == []
    assert len(db.get_recommendation_history()) == 1


def test_clear_recommendation_history(tmp_path):
    db = DatabaseRepository()
    db.database_name = tmp_path / "test_kpop.db"
    db.initialize_database()

    db.add_preference("artist", "aespa")
    db.save_recommendation("Howling", "XG")
    db.save_recommendation("Lemonade", "aespa")

    db.clear_recommendation_history()

    assert db.get_recommendation_history() == []
    assert db.get_preferences() == [("artist", "aespa")]