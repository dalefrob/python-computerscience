from pokemonbank import *
from PIL import Image
import random

# Load an image
img = Image.open('image.jpg')  # Replace 'image.jpg' with your image file path

# Display the image
img.show()

team = []

action_choice = input("Catch Pokemon: C, Battle Pokemon: B")

def catch_pokemon():
    random_pokemon = random.choice(allpokemon)
    team.append(random_pokemon.copy())

if action_choice == "C":
    catch_pokemon()


cpupokemon = random.choice(allpokemon)
print(f"CPU chooses {cpupokemon["name"]}!")

# Choose a pokemon from your team instead of all pokemon

print("Choose your pokemon!")
for i in range(len(team)):
    p = team[i]
    print(f"{i}:{p["name"]}")

chosen_index = int(input())
playerpokemon = team[chosen_index]

# Get the result from the battle and determine the winner

def battle(first_pokemon, second_pokemon):
    print(first_pokemon["name"], second_pokemon["name"])
    typeresult = typetable[first_pokemon["type"]][second_pokemon["type"]]
    print(typeresult)

battle(playerpokemon, cpupokemon)

# Modify the program so that you can choose the pokemon you will battle with DONE
# The opponent should be random DONE

# Redesign the win condition so a strong pokemon of a weaker type can still win