from services.recommendation_service import (
    get_candidate_tracks, 
    generate_recommendations, 
    filter_by_artist, 
    parse_tag_data, 
    filter_by_tag, 
    add_track_tags, 
    remove_unusable_tracks, 
    remove_duplicate_recommendations, 
    remove_previously_recommended, 
    parse_similar_artists, 
    generate_discovery_recommendations, 
    parse_artist_search_results, 
    parse_track_search_results,
    get_selectable_song_tags
)

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

def test_combined_recommendation_filters():
    recommendations = [
        {"title": "WOKE UP", "artist": "XG", "tags": ["rap", "hip hop"]},
        {"title": "LEFT RIGHT", "artist": "XG", "tags": ["rnb", "pop"]},
        {"title": "Drama", "artist": "aespa", "tags": ["dance", "k-pop"]},
        {"title": "Dynamite", "artist": "BTS", "tags": ["pop"]},
        {"title": "", "artist": "XG", "tags": ["rap"]}
    ]

    filtered = remove_unusable_tracks(recommendations)

    artist_filtered = filter_by_artist(filtered, ["XG", "aespa"])

    tag_filtered = filter_by_tag(artist_filtered, ["rap", "dance"])

    assert tag_filtered == [
        {"title": "WOKE UP", "artist": "XG", "tags": ["rap", "hip hop"]},
        {"title": "Drama", "artist": "aespa", "tags": ["dance", "k-pop"]}
    ]

def test_remove_duplicate_recommendations():
    recommendations = [
        {"title": "HOWLING", "artist": "XG"},
        {"title": "WOKE UP", "artist": "XG"},
        {"title": "howling", "artist": "xg"},
        {"title": "Drama", "artist": "aespa"}
    ]

    result = remove_duplicate_recommendations(recommendations)

    assert len(result) == 3
    assert result[0]["title"] == "HOWLING"
    assert result[1]["title"] == "WOKE UP"
    assert result[2]["title"] == "Drama"

def test_remove_previously_recommended():
    recommendations = [
        {"title": "HOWLING", "artist": "XG"},
        {"title": "WOKE UP", "artist": "XG"},
        {"title": "Drama", "artist": "aespa"}
    ]

    history = [
        ("howling", "xg", "2026-10-16 18:45:00"),
        ("Drama", "aespa", "2026-10-16 18:46:00")
    ]

    result = remove_previously_recommended(recommendations, history)

    assert len(result) == 1
    assert result[0]["title"] == "WOKE UP"
    assert result[0]["artist"] == "XG"

def test_remove_unusable_tracks():
    recommendations = [
        {"title": "Howling", "artist": "XG"},
        {"title": "", "artist": "aespa"},
        {"title": "Drama", "artist": ""},
        {"title": "   ", "artist": "XG"},
        {"title": "Woke Up", "artist": "XG"},
        {"title": None, "artist": "aespa"},
        {"artist": "XG"},
        {"title": "Song", "artist": 123}
    ]

    result = remove_unusable_tracks(recommendations)

    assert result == [
        {"title": "Howling", "artist": "XG"},
        {"title": "Woke Up", "artist": "XG"}
    ]


def test_remove_unusable_tracks_empty_list():
    assert remove_unusable_tracks([]) == []

def test_parse_similar_artists():
    response = {
        "similarartists": {
            "artist": [
                {"name": "Artist A", "match": "0.95"},
                {"name": "Artist B", "match": "0.82"},
                {"name": ""},
                {}
            ]
        }
    }

    result = parse_similar_artists(response)

    assert result == ["Artist A", "Artist B"]

def test_generate_discovery_recommendations():

    def mock_similar(artist_name):
        return {
            "similarartists": {
                "artist": [
                    {"name": "Similar Artist"},
                    {"name": "XG"}
                ]
            }
        }

    def mock_tracks(artist_name):
        return {
            "toptracks": {
                "track": [
                    {
                        "name": f"{artist_name} Song",
                        "artist": {"name": artist_name}
                    }
                ]
            }
        }

    result = generate_discovery_recommendations(
        ["aespa", "XG"],
        mock_similar,
        mock_tracks
    )

    assert result == [
        {"title": "aespa Song", "artist": "aespa"},
        {"title": "XG Song", "artist": "XG"},
        {"title": "Similar Artist Song", "artist": "Similar Artist"}
    ]

def test_parse_artist_search_results():
    response = {
        "results": {
            "artistmatches": {
                "artist": [
                    {"name": "aespa"},
                    {"name": "XG"},
                    {"name": ""}
                ]
            }
        }
    }

    result = parse_artist_search_results(response)

    assert len(result) == 2
    assert result[0] == {"type": "artist", "artist": "aespa", "title": None}
    assert result[1] == {"type": "artist", "artist": "XG", "title": None}

def test_parse_track_search_results():
    response = {
        "results": {
            "trackmatches": {
                "track": [
                    {"name": "Drama", "artist": "aespa"},
                    {"name": "WOKE UP", "artist": "XG"},
                    {"name": "", "artist": "Unknown Artist"}
                ]
            }
        }
    }

    result = parse_track_search_results(response)

    assert len(result) == 2
    assert result[0] == {"type": "track", "artist": "aespa", "title": "Drama"}
    assert result[1] == {"type": "track", "artist": "XG", "title": "WOKE UP"}

def test_get_selectable_song_tags():
    response = {
        "toptags": {
            "tag": [
                {"name": "k-pop"},
                {"name": "Electropop"},
                {"name": "K-POP"},
                {"name": ""},
                {"name": "dance"}
            ]
        }
    }

    result = get_selectable_song_tags(response)

    assert len(result) == 3
    assert result == ["k-pop", "Electropop", "dance"]