import os
import json

file_path = os.path.abspath(__file__) # absolute
file_directory = os.path.dirname(file_path)

output_dir = file_directory + "/output"

mypokemon = {
    "name": "Pikachu",
    "age": 9,
    "bestMove": "Thunderbolt"
}

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# with open(output_dir + "/myfile.txt", "a", encoding="utf-8") as file:
#     file.write("Hello again! \n")

def save(filename = "data"):
    with open(output_dir + f"/{filename}.json", "w") as file:
        json.dump(mypokemon, file)

def load(filename = "data"):
    with open(output_dir + f"/{filename}.json", "r") as file:
        mypokemon = json.load(file)
    return mypokemon #NOTE returns the data from this function

while True:
    choice = input("Save (s) or load (l)?")
    if choice == "l":
        result = load()  #NOTE <--- gets the data from the load function
        print("Loaded", result)
    elif choice == "s":
        save()
    else:
        break