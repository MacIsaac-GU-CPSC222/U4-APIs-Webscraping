import json
import requests
from urllib.parse import quote_plus
# Geocoding: 
# https://docs.mapbox.com/api/search/geocoding/

# Directions: 
# https://docs.mapbox.com/api/navigation/directions/

# python -m pip install requests json

def get_address_coords(addr):
    encoded_addr = quote_plus(addr)
    # print(encoded_addr)
    geocode_base_url = "https://api.mapbox.com/search/geocode/v6/forward?"
    url = geocode_base_url
    url += "q=" + encoded_addr
    url += "&access_token=" + mapbox_token

    # print(url)

    response = requests.get(url)
    json_obj = response.json()
    # print(json.dumps(json_obj, indent = 2))
    coords = json_obj["features"][0]["geometry"]["coordinates"]
    # print(coords)
    return coords

def get_directions(src_coords, dst_coords):
    direction_url = "https://api.mapbox.com/directions/v5/" 
    routing_profile = "mapbox/driving-traffic/"
    url = direction_url + routing_profile
    url += str(src_coords[0]) + "," + str(src_coords[1])
    url += ";"
    url += str(dst_coords[0]) + "," + str(dst_coords[1])
    url += "?access_token=" + mapbox_token
    print(url)

    response = requests.get(url)
    json_obj = response.json()
    # print(json.dumps(json_obj, indent=2))
    return json_obj

with open("secrets.json", "r") as f:
    creds = json.load(f)

# print(creds)
mapbox_token = creds["mapbox"]["public_id"]
print(f"token: {mapbox_token}")

gonzaga_address = "502 E Boone Ave, Spokane WA"
gonzaga_coords = get_address_coords(gonzaga_address)

mt_spo_address = "25211 N Mt Spokane Dr, Mead WA"
mt_spo_coords = get_address_coords(mt_spo_address)

print(f"Gonzaga coords: {gonzaga_coords}")
print(f"Mt Spo coords: {mt_spo_coords}")

json_directions = get_directions(gonzaga_coords, mt_spo_coords)

with open("directions_data.json", "w") as f:
    json.dump(json_directions, f, indent=4)


# TASK: parse the json object and print out the route distance in miles
route = json_directions["routes"][0]
print(route["distance"])
distance_miles = route["distance"] * 0.000621371
print(f"the distance of this route is {distance_miles:.2f} miles")
