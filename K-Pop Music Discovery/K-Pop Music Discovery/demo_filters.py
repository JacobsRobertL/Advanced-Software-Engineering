from services.recommendation_service import (
    filter_by_artist,
    filter_by_tag
)

tracks = [
    {"title": "HOWLING", "artist": "XG", "tags": ["dance", "pop"]},
    {"title": "Drama", "artist": "aespa", "tags": ["electronic", "pop"]},
    {"title": "FANCY", "artist": "TWICE", "tags": ["dance", "k-pop"]}
]

print("Artist filter:")
print(filter_by_artist(tracks, ["XG"]))

print("\nTag filter:")
print(filter_by_tag(tracks, ["dance"]))