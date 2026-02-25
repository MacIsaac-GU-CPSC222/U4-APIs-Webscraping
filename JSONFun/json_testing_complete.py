import json

j_file = open("climbing.json")
obj = json.load(j_file)
print(type(obj))
print(obj["climber"])
# get the climber's name


print(json.dumps(obj, indent=1))

print(obj["routes"])
print(obj["routes"][0]["sent"])

print(obj["notes"])

print(obj["total_time_minutes"])

# Task! Print out how many total attempts he completed

