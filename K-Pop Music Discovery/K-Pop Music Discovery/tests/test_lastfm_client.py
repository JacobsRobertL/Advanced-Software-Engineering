from unittest.mock import patch, Mock
from api.lastfm_client import get_similar_artists, search_artists, search_tracks


def test_get_similar_artists():
    mock_response = Mock()
    mock_response.json.return_value = {
        "similarartists": {
            "artist": [
                {"name": "Artist A", "match": "0.95"},
                {"name": "Artist B", "match": "0.82"}
            ]
        }
    }

    with patch("api.lastfm_client.requests.get") as mock_get:
        mock_get.return_value = mock_response

        result = get_similar_artists("aespa")

        assert len(result["similarartists"]["artist"]) == 2
        assert result["similarartists"]["artist"][0]["name"] == "Artist A"

        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args

        assert kwargs["params"]["method"] == "artist.getsimilar"
        assert kwargs["params"]["artist"] == "aespa"

        mock_response.raise_for_status.assert_called_once()

def test_search_artists():
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": {
            "artistmatches": {
                "artist": [
                    {"name": "aespa"},
                    {"name": "aespa Official"}
                ]
            }
        }
    }

    with patch("api.lastfm_client.requests.get") as mock_get:
        mock_get.return_value = mock_response

        result = search_artists("aespa")

        assert len(result["results"]["artistmatches"]["artist"]) == 2
        assert result["results"]["artistmatches"]["artist"][0]["name"] == "aespa"

        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args

        assert kwargs["params"]["method"] == "artist.search"
        assert kwargs["params"]["artist"] == "aespa"

        mock_response.raise_for_status.assert_called_once()

def test_search_tracks():
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": {
            "trackmatches": {
                "track": [
                    {"name": "Drama", "artist": "aespa"},
                    {"name": "Drama", "artist": "Other Artist"}
                ]
            }
        }
    }

    with patch("api.lastfm_client.requests.get") as mock_get:
        mock_get.return_value = mock_response

        result = search_tracks("Drama")

        assert len(result["results"]["trackmatches"]["track"]) == 2
        assert result["results"]["trackmatches"]["track"][0]["artist"] == "aespa"

        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args

        assert kwargs["params"]["method"] == "track.search"
        assert kwargs["params"]["track"] == "Drama"

        mock_response.raise_for_status.assert_called_once()
