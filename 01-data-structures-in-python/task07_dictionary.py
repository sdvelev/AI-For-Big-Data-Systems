
print(hash("b"))

dictionary = {}
another_dictionary = dict()

print(type(dictionary))
print(type(another_dictionary))
print(dictionary == another_dictionary)

dictionary["key1"] = "value1"
print(dictionary["key1"])

dictionary = {"key1" : "value1"}
print(dictionary["key1"])

dictionary = dict(key1 = "value1", key2 = "value2")
print(dictionary)

dictionary = dict([("key1", "value1"), ("key2", "value2")])
print(dictionary)

print(hash(1)) # Integer
print(hash(1.2)) # Float
print(hash("dataquest")) # String
print(hash((1, 2))) # Tuple
# print(hash([1, 2, 3])) List is mutable and cannot be hashed

dictionary[42] = "the answer to the ultimate question of life, the universe, and everything."
dictionary[1.2] = ["one point two"]
dictionary["list"] = ["just", "a", "list", "with", "an", "integer", 3]

print(dictionary)

dictionary["list"] = ["it's another", "list"]

print(dictionary)

duplicated_keys = {"key1": "value1", "key1": "value2", "key1": "value3"}

print(duplicated_keys["key1"])

harry_potter_dict = {
    "Harry Potter": "Gryffindor",
    "Ron Weasley": "Gryffindor",
    "Hermione Granger": "Gryffindor"
}

add_characters_1 = {
    "Albus Dumbledore": "Gryffindor",
    "Luna Lovegood": "Ravenclaw"
}

harry_potter_dict.update(add_characters_1)

print(harry_potter_dict)

add_characters_2 = [
    ["Draco Malfoy", "Slytherin"],
    ["Cedric Diggory", "Hufflepuff"]
]
harry_potter_dict.update(add_characters_2)

print(harry_potter_dict)

add_characters_3 = [
    ("Rubeus Hagrid", "Gryffindor"),
    ("Minerva McGonagall", "Gryffindor")
]

harry_potter_dict.update(add_characters_3)

print(harry_potter_dict)

del harry_potter_dict["Minerva McGonagall"]

print(harry_potter_dict)

# del harry_potter_dict["Voldemort"] There is not such a record in the dictionary

harry_potter_dict["Voldemort"] = "Slytherin"

print("Dictionary with Voldemort:")
print(harry_potter_dict)

# Remove the last inserted item (Voldemort)
harry_potter_dict.popitem()

print("Dictionary after popping the last inserted item (Voldemort):")
print(harry_potter_dict)

harry_potter_dict["Voldemort"] = "Slytherin"

print("Dictionary with Voldemort:")
print(harry_potter_dict)

# Remove the last inserted item (Voldemort)
print("Remove Voldemort and return his house:")
print(harry_potter_dict.pop("Voldemort"))

print("Dictionary after popping the last inserted item (Voldemort):")
print(harry_potter_dict)

print(harry_potter_dict.get("Harry Potter", "Key not found"))

print(harry_potter_dict.get("Voldemort", "Key not found"))

# print(harry_potter_dict["Voldemort"]) There is not a default value

print("Dictionary without Voldemort.")
print(harry_potter_dict)

print("Return the default value of Voldemort.")
print(harry_potter_dict.setdefault("Voldemort", "Slytherin"))

print("Voldemort is now in the dictionary!")
print(harry_potter_dict)

print(harry_potter_dict.items())

print(harry_potter_dict.keys())

print(harry_potter_dict.values())

for key, value in harry_potter_dict.items():
    print((key, value))

for key_value in harry_potter_dict.items():
    print(key_value)

for key, value in harry_potter_dict.items():
    print(f"The current key is {key} and its value is {value}.")

for key in harry_potter_dict.keys():
    print(key)

for value in harry_potter_dict.values():
    print(value)

from collections import Counter

counter = Counter(harry_potter_dict.values())
print(counter)

for k, v in counter.items():
    print((k, v))

from collections import defaultdict

default_d = defaultdict(list)

print(default_d["missing_key"])

for i in range(1, 6):
    default_d["missing_key"].append(f"value{i}")

print(default_d["missing_key"])

print(default_d)

d = {}
d.setdefault(0, 0)
print(d)
print(d.get(3, "three"))
print(d)