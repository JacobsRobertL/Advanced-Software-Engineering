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