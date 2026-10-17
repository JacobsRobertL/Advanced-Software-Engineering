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

if __name__ == "__main__":  #For testing purposes outside of a unit test framework
    artists = ["Aespa", "BTS", "Blackpink", "TWICE"]

    recommendations = generate_recommendations(artists, get_top_tracks)

    for track in recommendations:
        print(track)

    #from api.lastfm_client import get_top_tracks

    #candidates = get_candidate_tracks("Aespa", get_top_tracks)

    #for candidate in candidates:
    #    print(candidate)


