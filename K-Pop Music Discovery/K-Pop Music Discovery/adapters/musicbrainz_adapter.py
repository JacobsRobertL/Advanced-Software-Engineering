from api.musicbrainz_client import search_recording


class MusicBrainzAdapter:
    def __init__(self, fetch_recording=search_recording):
        self.fetch_recording = fetch_recording

    def get_recording_metadata(self, artist_name, track_name):
        response = self.fetch_recording(artist_name, track_name)
        recordings = response.get("recordings", [])

        if not recordings:
            return None

        recording = recordings[0]

        if int(recording.get("score", 0)) < 90:
            return None

        return {
            "title": recording.get("title"),
            "artist": artist_name,
            "musicbrainz_id": recording.get("id"),
            "match_score": recording.get("score", 0)
        }