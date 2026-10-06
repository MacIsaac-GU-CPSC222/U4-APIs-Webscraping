import json

j_file = open("climbing.json", "r")
j_obj = json.load(j_file)
j_file.close()

print(type(j_obj))

print(j_obj["climber"])
# task! Print the climber's name
print(j_obj["climber"]["name"])

print(json.dumps(j_obj, indent=2))

print(j_obj["routes"])
# task! Print out the name of the third route he climbed

print(j_obj["routes"][2]["name"])

print(j_obj["notes"])
print(j_obj["total_time_minutes"])
print(type(j_obj["total_time_minutes"]))

# task! Print out how many total attempts he completed

attempts = 0

for route in j_obj["routes"]:
    attempts += route["attempts"]

print(f"he did {attempts} attempts in todays session")

