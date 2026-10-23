import requests

BASE_URL = "https://musicbrainz.org/ws/2/"

HEADERS = {
    "User-Agent": "K-Pop Music Discovery/1.0 (contact: jacobsrobl@gmail.com)"
}

def search_artist(artist_name):
    url = f"{BASE_URL}artist/"
    
    params = {"query": artist_name, "fmt": "json"}

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def search_recording(artist_name, track_name):
    url = f"{BASE_URL}recording/"
    
    params = {"query": f'recording:"{track_name}" AND artist:"{artist_name}"', "fmt": "json", "limit": 5}

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)

    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # artist_name = "BTS"
    # result = search_artist(artist_name)
    # #print(result)

    # for artist in result.get("artists", []):
    #     print(artist["name"])

    result = search_recording("BTS", "Dynamite")

    for recording in result.get("recordings", []):
        print(
            recording.get("title"),
            recording.get("id"),
            recording.get("score")
        )