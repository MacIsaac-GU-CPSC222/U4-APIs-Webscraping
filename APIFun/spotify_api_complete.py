# Get access token: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
# Search for artist: https://developer.spotify.com/documentation/web-api/reference/search/search/

import base64
import requests
import json


with open("hide_creds.json", "r") as f:
        creds = json.load(f)

client_ID = creds["spotify"]["client_id"]
client_secret = creds["spotify"]["client_secret"]

auth_endpoint = "https://accounts.spotify.com/api/token"

def get_access_token():
    # from Spotify docs:
    # Required: Base 64 encoded string that contains the client ID and client secret key. 
    # The field must have the format: 
    # Authorization: Basic *<base64 encoded client_id:client_secret>*
    message = client_ID + ":" + client_secret
    # python string to bytes
    message_bytes = message.encode("ascii")

    # bytes to base64 bytes
    base64_bytes = base64.b64encode(message_bytes)
    
    #base64 bytes to string
    encoded_client_details = base64_bytes.decode("ascii")
    
    headers = {"Authorization": "Basic " + encoded_client_details}              
    body = {"grant_type": "client_credentials"}
    response = requests.post(url=auth_endpoint, headers=headers, data=body)
    json_object = json.loads(response.text)

    # print(json_object)
    return json_object["access_token"]


def get_artist_id(artist_name):
    # get token (client credentials)
    token = get_access_token()

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
    token = get_access_token()

    # get artist albums
    r = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/albums",
        headers={"Authorization": f"Bearer {token}"},  # change if you want more
        params={"limit":10}
    ).json()
    print(json.dumps(r, indent=5))
    albums = r["items"]
    album_names = [item["name"] for item in albums]
    # return a simple list of (album_name, album_id)
    return album_names



# tiny demo usage:
name = input("Artist name: ").strip()
id = get_artist_id(name)
print(id)
print(get_albums(id))
