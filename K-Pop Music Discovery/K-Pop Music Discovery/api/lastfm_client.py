import os
from pathlib import Path

import requests
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=ENV_PATH)

API_KEY = os.getenv("LASTFM_API_KEY")

BASE_URL = "http://ws.audioscrobbler.com/2.0/"


def get_artist_info(artist_name):
    parameters = {
        "method": "artist.getinfo",
        "artist": artist_name,
        "api_key": API_KEY,
        "format": "json",
    }
    response = requests.get(BASE_URL, params=parameters, timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    artist_name = "BTS"
    artist_info = get_artist_info(artist_name)
    print(artist_info)