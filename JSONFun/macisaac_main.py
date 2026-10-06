import json

j_file = open("climbing.json", "r")
obj = json.load(j_file)
j_file.close()
print(type(obj))
print(obj["climber"])
# get the climber's name
print(obj["climber"]["name"])

print(json.dumps(obj, indent=3))

print(obj["routes"])
print(obj["routes"][0]["sent"])

print(obj["notes"])

print(type(obj["total_time_minutes"]))

# Task! Print out how many total attempts he completed
attempts = 0
for route in obj["routes"]:
    attempts += route["attempts"]

print(f"total attempts: {attempts}")
