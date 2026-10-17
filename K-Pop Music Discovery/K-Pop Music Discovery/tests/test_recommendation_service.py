from services.recommendation_service import get_candidate_tracks, generate_recommendations, filter_by_artist

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


def test_generate_recommendations():
    # Mock the fetch_tracks function to return a predefined response
   def test_api(artist_name):
       return {
           "toptracks": {
                "track": [
                     {"name": f"{artist_name} Song", "artist": {"name": artist_name}},
                ]
              }
         }
   artist_names = ["XG", "NewJeans"]

   result = generate_recommendations(artist_names, test_api)

   assert result == [
       {"title": "XG Song", "artist": "XG"},
       {"title": "NewJeans Song", "artist": "NewJeans"}
   ]

def test_filter_by_artist():
    recommendations = [
        {"title": "Song 1", "artist": "XG"},
        {"title": "Song 2", "artist": "NewJeans"},
        {"title": "Song 3", "artist": "Mamamoo"},
    ]
    filtered = filter_by_artist(recommendations, ["XG", "NewJeans"])
    assert filtered == [
        {"title": "Song 1", "artist": "XG"},
        {"title": "Song 2", "artist": "NewJeans"}
    ]