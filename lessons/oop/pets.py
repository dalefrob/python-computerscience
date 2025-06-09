import random

# Colored text
# Try except finally?
# Class practice

# color
def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

class Food():
    def __init__(self, name, calories):
        self.name = name
        self.calories = calories

class Pet():
    def __init__(self, name : str, species : str = "cat"):
        self.name = name
        self.species = species

        self.hunger = 0

    def play(self, hours : int):
        print(colored(0,255,0,self.name), "plays for", hours, "hours")
    
    def feed(self, food : Food):
        text = f"{self.name} eats {food.name} ({food.calories} calories)"
        print(colored(255,255,0,text))
    
    def visit_vet(self):
        print(f"You take {self.name} to the vet")

    def on_new_day(self):
        if random.random() < 0.3:
            self.hunger += 1
        
        if self.hunger == 5:
            print(self.name, "is getting hungry")


# Tamagotchi

name = input("What is your pet's name?")
species = input("What is your pet's species?")
pet = Pet(name, species)


running = True
while running:
    option = input(f"What will you do? \n0: Feed {pet.name} \n1: Play with {pet.name}\n2: Take {pet.name} to the vet \n")
    try:
        intoption = int(option)
    except:
        running = False
        break

    match int(option):
        case 0: pet.feed()
        case 1: pet.play()
        case 2: pet.visit_vet()
        case _: running = False



