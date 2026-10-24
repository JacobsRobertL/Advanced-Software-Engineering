from adapters.musicbrainz_adapter import MusicBrainzAdapter


def test_musicbrainz_adapter_returns_metadata():
    def fake_search_recording(artist_name, track_name):
        return {
            "recordings": [
                {
                    "title": "Dynamite",
                    "id": "test-recording-id",
                    "score": 100
                }
            ]
        }

    adapter = MusicBrainzAdapter(fetch_recording=fake_search_recording)

    result = adapter.get_recording_metadata("BTS", "Dynamite")

    assert result == {
        "title": "Dynamite",
        "artist": "BTS",
        "musicbrainz_id": "test-recording-id",
        "match_score": 100
    }


def test_musicbrainz_adapter_handles_no_results():
    def fake_search_recording(artist_name, track_name):
        return {"recordings": []}

    adapter = MusicBrainzAdapter(fetch_recording=fake_search_recording)

    result = adapter.get_recording_metadata("BTS", "Unknown Song")

    assert result is None

def test_musicbrainz_adapter_rejects_low_score():
    def fake_search_recording(artist_name, track_name):
        return {
            "recordings": [
                {
                    "title": "Different Song",
                    "id": "incorrect-recording-id",
                    "score": 45
                }
            ]
        }

    adapter = MusicBrainzAdapter(fetch_recording=fake_search_recording)

    result = adapter.get_recording_metadata("BTS", "Dynamite")

    assert result is None