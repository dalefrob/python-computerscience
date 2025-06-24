import json
import os

# Get the full path of the current file
file_path = os.path.abspath(__file__)

# Get the folder (directory) that contains this file
file_directory = os.path.dirname(file_path)

newfiles_directory = file_directory + "/output"

number = 5
name = "Dale"
mylist = [1,2,3,4,5,6,7]
mydict = {
    "name": "Bob",
    "age": 33,
    "height": 150.6
}

def save():
    with open(newfiles_directory + "/output.json", "w") as f:
        json.dump(mydict, f, indent=4) # indent for pretty-printing

def load():
    with open(newfiles_directory + "/output.json", "r") as f:
        jsdict = json.load(f) 
    return jsdict


choice = input("save (s) or load (l) json?")
if choice == "s":
    save()
elif choice == "l":
    result = load()
    print("loaded!", result)
else:
    print("exiting...")