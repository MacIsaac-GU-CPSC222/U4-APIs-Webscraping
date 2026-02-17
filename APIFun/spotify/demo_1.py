import os
import sys
import base64
import requests
import json

import os, base64, requests

with open("spotify_creds.json", "r") as f:
        creds = json.load(f)
CID = creds["spotify"]["client_id"]
CSEC = creds["spotify"]["client_secret"]

def get_artist_id(artist_name: str) -> str | None:
    # get token (client credentials)
    auth = base64.b64encode(f"{CID}:{CSEC}".encode()).decode()
    token = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
    ).json()["access_token"]

    # search artist
    r = requests.get(
        "https://api.spotify.com/v1/search",
        headers={"Authorization": f"Bearer {token}"},
        params={"q": artist_name, "type": "artist", "limit": 1},
    ).json()

    items = r["artists"]["items"]
    return items[0]["id"] if items else None

def get_albums(artist_id):
    # get token (client credentials)
    auth = base64.b64encode(f"{CID}:{CSEC}".encode()).decode()
    token = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
    ).json()["access_token"]

    # get artist albums
    r = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/albums",
        headers={"Authorization": f"Bearer {token}"}  # change if you want more
    ).json()
    # print(r)

    # return a simple list of (album_name, album_id)
    return [(a["name"], a["id"]) for a in r["items"]]

def get_artist_top_tracks(artist_id, market="US"):
    # token (client credentials)
    auth = base64.b64encode(f"{CID}:{CSEC}".encode()).decode()
    token = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={"Authorization": f"Basic {auth}"},
        data={"grant_type": "client_credentials"},
    ).json()["access_token"]

    # top tracks for artist
    data = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
        headers={"Authorization": f"Bearer {token}"},
        params={"market": market},   # required
    ).json()
    print(data)
    
    # return simple list of (track_name, track_id)
    return [(t["name"], t["id"]) for t in data.get("tracks", [])]

def print_albums(albums):
     for name, id in albums:
        print(name)

# tiny demo usage:
name = input("Artist name: ").strip()
id = get_artist_id(name)
print(id)
print(print_albums(get_albums(id)))
print(get_artist_top_tracks(id))
