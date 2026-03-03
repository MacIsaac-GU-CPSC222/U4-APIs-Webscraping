# Get access token: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
# Search for artist: https://developer.spotify.com/documentation/web-api/reference/search/search/

import base64
import requests
import json

client_id = "550660ddc4c042b58b340b7b20db88e2"
client_secret = "1f0b728149f24be69abe713352b5bcba"

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

token = get_access_token()
print(token)
artist_id = get_artist_id("The Beatles", token)
albums = get_albums(artist_id, token)
print(albums)













# TASK! Fill out this function
def get_album_tracks(album_id):
    """
    Takes an Album ID and returns a list of the song names in that album

    Hint: You will need to look into the spotify albums documentation!
    """
    
    pass