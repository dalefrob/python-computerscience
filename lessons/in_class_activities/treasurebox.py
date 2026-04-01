import random

class Weapon:
    def __init__(self, name, damage, gold):
        self.name = name
        self.damage = damage
        self.gold = gold
    
    def __str__(self):
        return self.name



flail = Weapon("Flail of Flaying", 30, 155)
sword = Weapon("Sword of Death", 9999, 20000)

backpack = []

weapons = [sword, flail]

## Write a function to pick a  random weapon out of a list and return it
def get_random_weapon() -> dict:
    return random.choice(weapons)

for i in range(10):
    item = get_random_weapon()
    
    if item not in backpack:
        backpack.append(item)

for item in backpack:
    print(item)
