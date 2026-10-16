from services.recommendation_service import get_candidate_tracks

def test_get_candidate_tracks():
    # Mock the fetch_tracks function to return a predefined response
    test_response = {
        "toptracks": {
            "track": [
                {"name": "Illusion", "artist": {"name": "Aespa"}},
            ]
           }
    }

    def test_api(artist_name):
        assert artist_name == "Aespa"  # Ensure the correct artist name is passed
        return test_response

    # Call the function under test
    result = get_candidate_tracks("Aespa", test_api)

    # Define the expected result
    assert result == [{"title": "Illusion", "artist": "Aespa"}], f"Expected [{'title': 'Illusion', 'artist': 'Aespa'}], but got {result}"