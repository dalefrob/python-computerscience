import random

treasure_items = ["sword", "shield", "potion"] # The items in the box

backpack = {
    "sword": 0,
    "shield": 0,
    "potion": 0
}

def check_backpack():
    for item, amount in backpack.items():
        print(item, ":", amount)

def open_chest():
    item = random.choice(treasure_items)
    print(f"You got {item}")
    backpack[item] += 1   # backpack[item] = backpack[item] + 1

run_game = True
while run_game:
    print("0: Quit")
    print("1: Open Treasure Chest")
    print("2: Check Backpack")

    choice = int(input("Choose an action by number: ")) # Execution stops - blocking function
    if choice == 0:
        run_game = False
    elif choice == 1:
        open_chest()
    elif choice == 2:
        check_backpack()
    elif choice == 10:  # Opens 10 chests!!
        for i in range(10):
            open_chest()

print("Exiting game")