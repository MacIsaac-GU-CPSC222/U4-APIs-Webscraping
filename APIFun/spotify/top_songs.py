# Artist Explorer Demo (Client Credentials / Basic Spotify Web API)
# - Search artist (show top matches)
# - Show genres / popularity / followers
# - Show albums/singles
# - Show top tracks (fallback to track-search if /top-tracks is blocked)

import requests
import json
import base64
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

AUTH_ENDPOINT = "https://accounts.spotify.com/api/token"
SEARCH_ENDPOINT = "https://api.spotify.com/v1/search"
ARTIST_ENDPOINT = "https://api.spotify.com/v1/artists/{id}"
ARTIST_ALBUMS_ENDPOINT = "https://api.spotify.com/v1/artists/{id}/albums"
ARTIST_TOP_TRACKS_ENDPOINT = "https://api.spotify.com/v1/artists/{id}/top-tracks"


@dataclass
class SpotifyAPIError(Exception):
    status: int
    message: str
    body: Any

    def __str__(self):
        return f"Spotify API error {self.status}: {self.message}"


def load_credentials(json_path: str = "spotify_creds.json") -> Tuple[str, str]:
    with open(json_path, "r") as f:
        creds = json.load(f)

    if "client_id" in creds and "client_secret" in creds:
        return creds["client_id"], creds["client_secret"]

    if "spotify" in creds and "client_id" in creds["spotify"] and "client_secret" in creds["spotify"]:
        return creds["spotify"]["client_id"], creds["spotify"]["client_secret"]

    raise ValueError(
        f"Could not find client_id/client_secret in {json_path}. "
        "Expected keys: client_id, client_secret (optionally nested under 'spotify')."
    )


def get_access_token(client_id: str, client_secret: str) -> str:
    message = f"{client_id}:{client_secret}".encode("ascii")
    encoded = base64.b64encode(message).decode("ascii")

    headers = {"Authorization": "Basic " + encoded}
    data = {"grant_type": "client_credentials"}

    resp = requests.post(AUTH_ENDPOINT, headers=headers, data=data, timeout=15)
    try:
        body = resp.json()
    except Exception:
        body = resp.text

    if resp.status_code != 200:
        msg = body.get("error_description") if isinstance(body, dict) else str(body)
        raise SpotifyAPIError(resp.status_code, msg or "Token request failed", body)

    if "access_token" not in body:
        raise SpotifyAPIError(resp.status_code, "No access_token in response", body)

    return body["access_token"]


def make_request(access_token: str, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    headers = {"Authorization": "Bearer " + access_token}
    resp = requests.get(url, headers=headers, params=params, timeout=15)

    # Handle rate limiting cleanly
    if resp.status_code == 429:
        retry_after = resp.headers.get("Retry-After", "?")
        raise SpotifyAPIError(429, f"Rate limited. Retry-After: {retry_after}s", resp.text)

    try:
        body = resp.json()
    except Exception:
        body = {"raw": resp.text}

    if resp.status_code >= 400:
        # Debug info that reveals the *actual* URL Spotify received
        print("\n--- DEBUG ---")
        print("REQUEST URL:", resp.url)
        print("STATUS:", resp.status_code)
        print("PARAMS SENT:", params)
        print("RESPONSE:", body)
        print("-------------\n")

        if isinstance(body, dict) and "error" in body and isinstance(body["error"], dict):
            err = body["error"]
            raise SpotifyAPIError(resp.status_code, err.get("message", "Request failed"), body)

        raise SpotifyAPIError(resp.status_code, "Request failed", body)

    return body


def search_artists(access_token: str, artist_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    # sanitize limit (Spotify expects 1..50)
    limit = int(limit)
    limit = max(1, min(limit, 50))

    params = {"q": artist_name, "type": "artist", "limit": limit}
    data = make_request(access_token, SEARCH_ENDPOINT, params=params)
    return data.get("artists", {}).get("items", [])


def pick_artist_interactively(items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not items:
        return None

    print("\nTop matches:")
    for i, a in enumerate(items, start=1):
        name = a.get("name", "UNKNOWN")
        popularity = a.get("popularity", "N/A")
        followers = a.get("followers", {}).get("total", "N/A")
        print(f"  {i}. {name} | popularity={popularity} | followers={followers}")

    choice = input("Pick a number (Enter for 1): ").strip()
    if choice == "":
        return items[0]

    try:
        idx = int(choice)
        if 1 <= idx <= len(items):
            return items[idx - 1]
    except ValueError:
        pass

    print("Invalid choice; defaulting to 1.")
    return items[0]


def get_artist(access_token: str, artist_id: str) -> Dict[str, Any]:
    url = ARTIST_ENDPOINT.format(id=artist_id)
    return make_request(access_token, url)


def get_artist_albums(access_token: str, artist_id: str, market: str = "US", limit: int = 20) -> List[Dict[str, Any]]:
    # ✅ Fix for your crash: enforce int + clamp 1..50
    try:
        limit = int(limit)
    except Exception:
        limit = 20
    limit = max(1, min(limit, 50))

    url = ARTIST_ALBUMS_ENDPOINT.format(id=artist_id)
    params = {
        "include_groups": "album,single",
        "market": market,
        "limit": limit,
    }
    data = make_request(access_token, url, params=params)
    items = data.get("items", [])

    # De-duplicate common duplicates
    seen = set()
    unique = []
    for alb in items:
        key = (alb.get("name", "").lower(), alb.get("release_date", ""))
        if key in seen:
            continue
        seen.add(key)
        unique.append(alb)
    return unique


def get_top_tracks(access_token: str, artist_id: str, market: str = "US") -> List[Dict[str, Any]]:
    url = ARTIST_TOP_TRACKS_ENDPOINT.format(id=artist_id)
    try:
        data = make_request(access_token, url, params={"market": market})
        return data.get("tracks", [])
    except SpotifyAPIError as e:
        # Many people are seeing 403 on this endpoint in some environments
        if e.status == 403:
            return []
        raise


def get_top_tracks_fallback_search(access_token: str, artist_name: str, market: str = "US", limit: int = 10) -> List[Dict[str, Any]]:
    # sanitize limit
    limit = int(limit)
    limit = max(1, min(limit, 50))

    params = {
        "q": f'artist:"{artist_name}"',
        "type": "track",
        "market": market,
        "limit": limit,
    }
    data = make_request(access_token, SEARCH_ENDPOINT, params=params)
    return data.get("tracks", {}).get("items", [])


def print_artist_summary(artist: Dict[str, Any]) -> None:
    name = artist.get("name", "UNKNOWN")
    popularity = artist.get("popularity", "N/A")
    followers = artist.get("followers", {}).get("total", "N/A")
    genres = artist.get("genres", []) or []

    print("\n====================")
    print(f"Artist: {name}")
    print(f"Popularity: {popularity}")
    print(f"Followers: {followers}")
    print(f"Genres: {genres if genres else '[]'}")
    print("====================\n")


def print_albums(albums: List[Dict[str, Any]], max_items: int = 10) -> None:
    print(f"Albums/Singles (showing up to {max_items}):")
    for i, a in enumerate(albums[:max_items], start=1):
        name = a.get("name", "UNKNOWN")
        release = a.get("release_date", "N/A")
        album_type = a.get("album_type", "N/A")
        print(f"  {i:>2}. {name} ({album_type}, {release})")
    print()


def print_tracks(tracks: List[Dict[str, Any]], max_items: int = 10) -> None:
    print(f"Top Tracks (showing up to {max_items}):")
    for i, t in enumerate(tracks[:max_items], start=1):
        name = t.get("name", "UNKNOWN")
        popularity = t.get("popularity", "N/A")
        album = t.get("album", {}).get("name", "UNKNOWN ALBUM")
        preview = t.get("preview_url")
        if preview:
            print(f"  {i:>2}. {name} | pop={popularity} | album={album} | preview={preview}")
        else:
            print(f"  {i:>2}. {name} | pop={popularity} | album={album}")
    print()


def main():
    client_id, client_secret = load_credentials("spotify_creds.json")
    token = get_access_token(client_id, client_secret)

    artist_name = input("Enter an artist name: ").strip()
    if not artist_name:
        print("No artist entered.")
        return

    matches = search_artists(token, artist_name, limit=5)
    picked = pick_artist_interactively(matches)
    if not picked:
        print(f"No artists found for: {artist_name}")
        return

    artist_id = picked.get("id")
    if not artist_id:
        print("No artist ID found in search result.")
        return

    full_artist = get_artist(token, artist_id)
    print_artist_summary(full_artist)

    albums = get_artist_albums(token, artist_id, market="US", limit=20)
    print_albums(albums, max_items=10)

    tracks = get_top_tracks(token, artist_id, market="US")
    if not tracks:
        print("(Note: /top-tracks unavailable (often 403). Using search fallback.)\n")
        tracks = get_top_tracks_fallback_search(token, full_artist.get("name", artist_name), market="US", limit=10)

    print_tracks(tracks, max_items=10)


if __name__ == "__main__":
    main()