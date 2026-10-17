from database.db_repository import DatabaseRepository

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