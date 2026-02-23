import json

json_s = '{"name": "John", "age": 25, "test items":["wonky", 123, true, null, false]}'
json_y = '[{"name":"Bill", "age":30}, {"name":"Sarah", "age":29}]'

obj = json.loads(json_s)
name = obj["name"]
age = obj["age"]
print(type(obj))

print(f"Name: {name}, Age: {age}")
print(obj["test items"])

obj = json.loads(json_y)
print(obj[0]["name"])

j_file = open("climbing.json")
obj = json.load(j_file)
print(obj["routes"])