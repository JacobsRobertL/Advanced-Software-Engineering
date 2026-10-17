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

def parse_tag_data(response):
    tags = response.get("toptags", {}).get("tag", [])
    tag_list = []
    
    for tag in tags:
        tag_name = tag.get("name")
        
        if tag_name:
            tag_list.append(tag_name)

    return tag_list

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

def filter_by_tag(recommendations, tag_name):
    filtered = []
    
    for track in recommendations:
        for tag in track.get("tags", []):
            if tag.lower() in [name.lower() for name in tag_name]:
                filtered.append(track)
                break

    return filtered

def add_track_tags(recommendations, fetch_tags):
    for track in recommendations:
        response = fetch_tags(track["artist"], track["title"])
        track["tags"] = parse_tag_data(response)
    
    return recommendations

def remove_unusable_tracks(recommendations):
    valid = []

    for track in recommendations:
        title = track.get("title")
        artist = track.get("artist")

        if isinstance(title, str) and isinstance(artist, str) and title.strip() and artist.strip():
            valid.append(track)

    return valid

if __name__ == "__main__":  #For testing purposes outside of a unit test framework
    # TEMP
    # artists = ["XG", "NewJeans", "Mamamoo"]

    # recommendations = generate_recommendations(artists, get_top_tracks)

    # filtered = filter_by_artist(recommendations, ["XG", "NewJeans"])

    # for track in filtered:
    #     print(track)

    # TEMP
    #from api.lastfm_client import get_top_tracks

    #candidates = get_candidate_tracks("Aespa", get_top_tracks)

    #for candidate in candidates:
    #    print(candidate)

    # TEMP
    from api.lastfm_client import get_song_tags

    # tag_data = get_song_tags("XG", "Woke Up")
    # tags = parse_tag_data(tag_data)
    # print(tags)

    # recommendations = [
    #     {"title": "Song 1", "artist": "XG", "tags": ["k-pop", "rap"]},
    #     {"title": "Song 2", "artist": "NewJeans", "tags": ["k-pop", "pop"]},
    #     {"title": "Song 3", "artist": "Mamamoo", "tags": ["hip-hop", "pop"]}
    # ]

    # filtered = filter_by_tag(recommendations, ["hip-hop", "rap"])

    # for track in filtered:
    #     print(track)

    # TEMP
    # recommendations = generate_recommendations(["XG"], get_top_tracks)
    # recommendations = add_track_tags(recommendations, get_song_tags)

    # filtered = filter_by_tag(recommendations, ["rap", "dance"])

    # for track in filtered:
    #     print(track)

    # print(f"Matching tracks: {len(filtered)}")

    # TEMP
    recommendations = [
    {"title": "WOKE UP", "artist": "XG", "tags": ["rap"]},
    {"title": "", "artist": "aespa", "tags": ["k-pop"]},
    {"title": "Drama", "artist": "", "tags": ["dance"]},
    {"title": "MASCARA", "artist": "XG", "tags": []}
    ]

    valid_recommendations = remove_unusable_tracks(recommendations)
    for track in valid_recommendations:
        print(track)
