from unittest.mock import patch, Mock

from api.musicbrainz_client import search_recording


def test_search_recording():
    mock_response = Mock()
    mock_response.json.return_value = {
        "recordings": [
            {
                "title": "Dynamite",
                "id": "test-mbid-123",
                "score": 100
            }
        ]
    }

    with patch("api.musicbrainz_client.requests.get") as mock_get:
        mock_get.return_value = mock_response

        result = search_recording("BTS", "Dynamite")

        assert result == mock_response.json.return_value

        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args

        assert args[0] == "https://musicbrainz.org/ws/2/recording/"
        assert kwargs["params"]["query"] == 'recording:"Dynamite" AND artist:"BTS"'
        assert kwargs["params"]["fmt"] == "json"
        assert kwargs["params"]["limit"] == 5

        mock_response.raise_for_status.assert_called_once()