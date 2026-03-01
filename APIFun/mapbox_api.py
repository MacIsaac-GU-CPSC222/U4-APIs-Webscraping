import json
import requests
from urllib.parse import quote_plus

# Get key to use API

with open("hide_creds.json", "r") as f:
    creds = json.load(f)

# mapbox_public_id = "...."

mapbox_public_id = creds["mapbox"]["public_id"]

print(mapbox_public_id)

def get_address_coords(addr):
    """
    Takes an address and returns the latitude and longitude of that location
    """
    encoded_addr = quote_plus(addr)
    # print(encoded_addr)
    geocode_base_url = "https://api.mapbox.com/search/geocode/v6/forward?"
    url = geocode_base_url
    url += "q=" + encoded_addr
    url += "&access_token=" + mapbox_public_id
    # print(url)

    response = requests.get(url)
    # print(response)
    json_obj = response.json()
    # print(json.dumps(json_obj, indent = 2))

    coords = json_obj["features"][0]["properties"]["coordinates"]
    # print(coords)
    return coords

def get_directions(src_coords, dst_coords):
    direction_url = "https://api.mapbox.com/directions/v5/"
    url = direction_url + "mapbox/cycling/"
    url += str(src_coords["longitude"]) + "," + str(src_coords["latitude"])
    url += ";"
    url += str(dst_coords["longitude"]) + "," + str(dst_coords["latitude"])

    url += "?access_token=" + mapbox_public_id

    print(url)
    response = requests.get(url)
    json_obj = response.json()
    # print(json.dumps(json_obj, indent = 2))
    return json_obj

# Get source and destination addresses
src_addr = "502 E Boone Ave, Spokane,WA"
dst_addr = "25211 N Mt Spokane Dr, Mead, WA"

src_coords = get_address_coords(src_addr)
dst_coords = get_address_coords(dst_addr)
# Geocoding time! Address to Coordinates
json_directions = get_directions(src_coords, dst_coords)



# Now lets get directions from the source to the destination



# TODO  TASK: parse the json object (dictionary) and print out 
#       the route distance in miles 

route = json_directions["routes"][0]
print(route)

distance_miles = route["distance"] * 0.000621371
# get the first route object
print(f"the distance of this route is {distance_miles:.2f} miles")

# TODO Task: 

