from services.recommendation_service import get_candidate_tracks, generate_recommendations, filter_by_artist, parse_tag_data, filter_by_tag, add_track_tags, remove_unusable_tracks

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

def test_parse_tag_data():
    response = {
        "toptags": {
            "tag": [
                {"name": "k-pop", "count": 100},
                {"name": "dance", "count": 80},
                {"name": "pop", "count": 60}
            ]
        }
    }
    tags = parse_tag_data(response)
    assert tags == ["k-pop", "dance", "pop"]

def test_filter_by_tag():
    recommendations = [
        {"title": "Song 1", "artist": "XG", "tags": ["k-pop", "rap"]},
        {"title": "Song 2", "artist": "NewJeans", "tags": ["k-pop", "dance"]},
        {"title": "Song 3", "artist": "Mamamoo", "tags": ["hip-hop", "pop"]},
    ]
    filtered = filter_by_tag(recommendations, ["RAP", "DANCE"])
    assert filtered == [
        {"title": "Song 1", "artist": "XG", "tags": ["k-pop", "rap"]},
        {"title": "Song 2", "artist": "NewJeans", "tags": ["k-pop", "dance"]}
    ]

def test_add_track_tags():
    recommendations = [
        {"title": "WOKE UP", "artist": "XG"},
        {"title": "Drama", "artist": "aespa"}
    ]
    def test_tag_api(artist_name, track_name):
        if artist_name == "XG" and track_name == "WOKE UP":
            return {
                "toptags": {
                    "tag": [
                        {"name": "rap"},
                        {"name": "hip hop"}
                    ]
                }
            }

        return {"toptags": {"tag": []}}  # Return empty tags for other tracks}

    result = add_track_tags(recommendations, test_tag_api)
    assert result == [
        {"title": "WOKE UP", "artist": "XG", "tags": ["rap", "hip hop"]},
        {"title": "Drama", "artist": "aespa", "tags": []}
    ]

def test_remove_unusable_tracks():
    recommendations = [
        {"title": "WOKE UP", "artist": "XG", "tags": ["rap"]},
        {"title": "", "artist": "aespa"},
        {"title": "Drama", "artist": ""},
        {"title": "   ", "artist": "BTS"},
        {"title": "MASCARA", "artist": "XG", "tags": []},
        {"artist": "TWICE"},
        {"title": "Supernova", "artist": None}
    ]

    result = remove_unusable_tracks(recommendations)

    assert result == [
        {"title": "WOKE UP", "artist": "XG", "tags": ["rap"]},
        {"title": "MASCARA", "artist": "XG", "tags": []}
    ]