import json

j_file = open("climbing.json")
obj = json.load(j_file)
j_file.close()

print(type(obj))
print(type(obj["climber"]["age"]))

# print(json.dumps(obj, indent = 2))

print(len(obj["routes"]))

print(obj["notes"])

# Task! Print out how many total attempts this climber attempted 
total_attempts = 0
# total_attempts += obj["routes"][0]["attempts"]
for route in obj["routes"]:
    total_attempts += route["attempts"]


print(f"total attempts: {total_attempts}")