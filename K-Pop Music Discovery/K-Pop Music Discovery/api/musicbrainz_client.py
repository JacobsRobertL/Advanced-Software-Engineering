import requests

BASE_URL = "https://musicbrainz.org/ws/2/"

HEADERS = {
    "User-Agent": "K-Pop Music Discovery/1.0 (contact: jacobsrobl@gmail.com)"
}

def search_artist(artist_name):
    url = f"{BASE_URL}artist/"
    params = {
        "query": artist_name,
        "fmt": "json"
    }
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    artist_name = "BTS"
    result = search_artist(artist_name)
    print(result)