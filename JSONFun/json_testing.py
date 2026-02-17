import json

json_s = '{"name": "John", "age": 25, "test items":["wonky", 123, true, null, false]}'

obj = json.loads(json_s)
name = obj["name"]
age = obj["age"]
print(type(obj))

print(f"Name: {name}, Age: {age}")
print(obj["dogs"])