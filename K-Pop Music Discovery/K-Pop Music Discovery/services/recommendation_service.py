from api.lastfm_client import get_artist_info, get_top_tracks

def parse_track_data(response):
    tracks = response.get("toptracks", {}).get("track", [])
    candidates = []

    for track in tracks:
        title = track.get("name")
        artist = track.get("artist", {}).get("name")
        
        if title and artist:
            candidates.append({"title": title, "artist": artist})

    return candidates

def get_candidate_tracks(artist_name, fetch_tracks):
    response = fetch_tracks(artist_name)
    return parse_track_data(response)

