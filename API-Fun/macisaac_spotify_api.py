# Get access token: 
#   https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow
#   - POST is used to send data to a server to create/update a resource.
#   https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
#   https://developer.spotify.com/documentation/web-api/concepts/access-token
#   https://softuni.org/wp-content/uploads/2022/07/HTTP-Requests-Example.png

# Search for artist: https://developer.spotify.com/documentation/web-api/reference/search
# Get Artist's Albums: https://developer.spotify.com/documentation/web-api/reference/get-an-artists-albums
# Get Album Tracks: https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks
import base64
import requests
import json

with open("secrets.json", "r") as s:
    secrets_dict = json.load(s)

client_id = secrets_dict["spotify"]["client_id"]
client_secret = secrets_dict["spotify"]["client_secret"]

def get_access_token():
    # from Spotify docs:
    # Required: Base 64 encoded string that contains the client ID and client secret key. 
    # The field must have the format: 
    # Authorization: Basic *<base64 encoded client_id:client_secret>*

    
    message = client_id + ":" + client_secret

    message_bytes = message.encode("ascii")

    base_64_bytes = base64.b64encode(message_bytes)

    encoded_message = base_64_bytes.decode("ascii")

    headers = {"Authorization": "Basic " + encoded_message}
    body = {"grant_type": "client_credentials"}
    endpoint = "https://accounts.spotify.com/api/token"

    response = requests.post(url=endpoint, headers=headers, data=body)
    js = response.json()

    return js["access_token"]

def get_artist_id(artist_name, token):
    r = requests.get(
    "https://api.spotify.com/v1/search", 
    
    params = {"q":artist_name, "type":"artist","limit": 1},
    
    headers={"Authorization": f"Bearer {token}"}
    )
    js = r.json()
    # print(json.dumps(js, indent=4))

    return js["artists"]["items"][0]["id"]

def get_albums(artist_id, token):
    r = requests.get(
    f"https://api.spotify.com/v1/artists/{artist_id}/albums",
    headers={"Authorization": f"Bearer {token}"},
    params = {"limit":10}
    )
    js = r.json()
    # print(json.dumps(js, indent = 5))
    albums = js["items"]
    album_names = [
     (album["name"], album["id"]) for album in albums
    ]
    return album_names

def get_album_tracks(album_id, token):

    # get artist albums
    r = requests.get(
        f"https://api.spotify.com/v1/albums/{album_id}/tracks",
        headers={"Authorization": f"Bearer {token}"},  # change if you want more
        params={}
    ).json()
    print(json.dumps(r, indent=5))
    songs = [item["name"] for item in r["items"]]
    return songs

token = get_access_token()
print(token)
name = input("Artist name: ").strip()
id = get_artist_id(name, token)
print(id)
albums = get_albums(id, token)
print(albums)
tracks = get_album_tracks(albums[0][1], token)
print(tracks)




