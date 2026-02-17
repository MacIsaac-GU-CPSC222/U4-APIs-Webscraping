import json
import requests
from urllib.parse import quote_plus

# Get key to use API
with open("hide_creds.json", "r") as f:
        creds = json.load(f)

mapbox_public_id = creds["mapbox"]["public_id"]

print(mapbox_public_id)


def get_address_coords(addr):
    # Our address has spaces and such in it that do no work with URLs
    # so we need to modify them (replacing spaces with )
    encoded_address = quote_plus(addr)
    print(encoded_address)

    geocode_base_url = "https://api.mapbox.com/search/geocode/v6/forward"
    url = geocode_base_url+ "?q="
    url += encoded_address
    url += "&access_token=" + mapbox_public_id

    print(url)

    response = requests.get(url)

    json_obj = response.json()

    print(json.dumps(json_obj, indent=5))

    coords = json_obj["features"][0]["properties"]["coordinates"]

    return coords


def get_directions(src_coords, dst_coords):
    directions_base_url = "https://api.mapbox.com/directions/v5/"
    url = directions_base_url + "mapbox/driving/"
    url += str(src_coords["longitude"]) + "," + str(src_coords["latitude"])
    url += ";"
    url += str(dst_coords["longitude"]) + "," + str(dst_coords["latitude"])

    # url += "-117.4115166,47.6730239;-116.7583938,47.6641004" 
    url += "?access_token="+ mapbox_public_id
    print(url)

    response = requests.get(url)

    json_obj = response.json()

    print(json.dumps(json_obj, indent=5))
    
    return json_obj


# Get source and destination addresses
src_addr = input("Enter source address: ") # 502 E Boone Ave, Spokane, WA
dst_addr = input("Enter destination address: ") # 25211 N Mt Spokane Dr, Mead, WA

# Geocoding time! Address to Coordinates
src_coords = get_address_coords(src_addr)
dst_coords = get_address_coords(dst_addr)

print(src_coords["longitude"], src_coords["latitude"])
print(dst_coords["longitude"], dst_coords["latitude"])


# Now lets get directions from the source to the destination
json_directions = get_directions(src_coords, dst_coords)


# TASK: parse the json object (dictionary) and print out
# the route distance in miles 

# get the first route object
route = json_directions["routes"][0]

# print(route)

# what unit is distance in? Check the docs!
distance_miles = route["distance"] * 0.000621371
print(f"Distance miles: {distance_miles:.2f} miles")

