from unittest.mock import patch, Mock
from api.lastfm_client import get_similar_artists


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