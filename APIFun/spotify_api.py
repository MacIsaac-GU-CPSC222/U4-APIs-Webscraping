# Get access token: https://developer.spotify.com/documentation/general/guides/authorization-guide/#client-credentials-flow
# Search for artist: https://developer.spotify.com/documentation/web-api/reference/search/search/

import base64
import requests
import json


def get_access_token():
    # from Spotify docs:
    # Required: Base 64 encoded string that contains the client ID and client secret key. 
    # The field must have the format: 
    # Authorization: Basic *<base64 encoded client_id:client_secret>*
    pass
