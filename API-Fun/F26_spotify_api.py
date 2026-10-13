# Get access token: 
#   - https://developer.spotify.com/documentation/web-api/tutorials/client-credentials-flow
#   - POST is used to send data to a server to create/update a resource.
#   - https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
#   - https://developer.spotify.com/documentation/web-api/concepts/access-token
#   - https://softuni.org/wp-content/uploads/2022/07/HTTP-Requests-Example.png

# Search for artist: https://developer.spotify.com/documentation/web-api/reference/search
# Get Artist's Albums: https://developer.spotify.com/documentation/web-api/reference/get-an-artists-albums
# Get Album Tracks: https://developer.spotify.com/documentation/web-api/reference/get-an-albums-tracks
import base64
import requests
import json

with open("secrets.json", "r") as s_file:
    secrets_dict = json.load(s_file)

client_id = secrets_dict["spotify"]["client_id"]
client_secret = secrets_dict["spotify"]["client_secret"]
print(client_id)
print(client_secret)

def get_access_token():
    message = client_id + ":" + client_secret
    message_bytes = message.encode("ascii")
    base_64_bytes = base64.b64encode(message_bytes)
    encoded_message = base_64_bytes.decode("ascii")

    headers = {"Authorization":"Basic " + encoded_message}
    body = {"grant_type": "client_credentials"}
    endpoint = "https://accounts.spotify.com/api/token"

    response = requests.post(url=endpoint, headers=headers, data=body)
    js = response.json()
    # print(js)
    return js["access_token"]

def get_artist_id(artist_name, token):
    response = requests.get(
        "https://api.spotify.com/v1/search",
        params = {"q":artist_name, "type":"artist", "limit": 1},
        headers = {"Authorization": f"Bearer {token}"})

    js = response.json()
    # print(json.dumps(js, indent = 2))
    return js["artists"]["items"][0]["id"]

def get_albums(artist_id, token):
    response = requests.get(
        f"https://api.spotify.com/v1/artists/{artist_id}/albums",
        headers= {"Authorization": f"Bearer {token}"},
        params = {"limit": 10}
    )
    print(response)
    js = response.json()
    # print(json.dumps(js, indent=2))
    albums = js["items"]
    albums_returns = []
    for album in albums:
        albums_returns.append((album["name"], album["id"]))
    return albums_returns

# TASK! Fill out this function
def get_album_tracks(album_id, token):
    """
    Takes an Album ID and returns a list of the song names in that album
    Hint: You will need to look into the spotify albums documentation!
    """
    r = requests.get(
        f"https://api.spotify.com/v1/albums/{album_id}/tracks",
        headers= {"Authorization": f"Bearer {token}"},
        params = {"limit": 10}
    )
    print(r)
    js = r.json()
    # print(json.dumps(js, indent=2))

    songs_json = js["items"]
    songs = []
    for song_json in songs_json:
        songs.append(song_json["name"])
    return songs

def main():
    token = get_access_token()
    print(f"token: {token}")
    artist = "Hockey Dad"
    id = get_artist_id(artist, token)
    albums = get_albums(id, token)
    print(albums)
    album_tracks = get_album_tracks(albums[0][1], token)
    print(album_tracks)

main()



