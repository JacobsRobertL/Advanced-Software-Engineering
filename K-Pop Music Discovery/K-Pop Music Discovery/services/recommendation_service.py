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


def generate_recommendations(artist_names, fetch_tracks):
    recommendations = []

    for artist in artist_names:
        candidates = get_candidate_tracks(artist, fetch_tracks)
        recommendations.extend(candidates)

    return recommendations

def filter_by_artist(recommendations, artist_name):
    filtered = []
    
    for track in recommendations:
        artist = track["artist"]
        
        if artist.lower() in [name.lower() for name in artist_name]:
            filtered.append(track)

    return filtered

if __name__ == "__main__":  #For testing purposes outside of a unit test framework
    artists = ["XG", "NewJeans", "Mamamoo"]

    recommendations = generate_recommendations(artists, get_top_tracks)

    filtered = filter_by_artist(recommendations, ["XG", "NewJeans"])

    for track in filtered:
        print(track)

    #from api.lastfm_client import get_top_tracks

    #candidates = get_candidate_tracks("Aespa", get_top_tracks)

    #for candidate in candidates:
    #    print(candidate)


