import random

special = {
    "health potion": {
        "name": "Potion of Health 🍺",
        "add-health": 10 
    },
}

# List of possible treasures
treasure = ["ruby", "sapphire", "gold", "emerald", "health potion"]

# Dictionary to store the inventory
inventory = {}

# Function to open a treasure box and get a random item
def open_treasure_box():
    if random.random() < 0.2:
        thief_steal()
        return
    item = random.choice(treasure)  # Pick a random item from the list
    amount = 1
    if item == treasure[2]:
        amount = random.randrange(1, 50)
    if item in inventory:
        inventory[item] += amount
    else:
        inventory[item] = amount
    print(f"You found {amount} {item}!")

def thief_steal():
    if len(inventory) > 0:
        key, amount = inventory.popitem()
        print(f"!! A thief steals {amount} {key}(s) !!")
    else:
        print("A theif tries to steal from you, but you have nothing.")

# Function to display the inventory
def display_inventory():
    if inventory:
        print("\nYour Inventory:")
        for item, count in inventory.items():
            print(f"{item}: {count}")
            if item in special:
                print(special[item]["name"])
    else:
        print("\nYour inventory is empty.")

def sell_item():
    if len(inventory.keys()) == 0:
        print("Nothing to sell!")
        return
    if len(inventory.keys()) == 1:
        if list(inventory.keys())[0] == "gold":
            print("Nothing to sell!")
            return
    display_inventory()
    item_to_sell = input("\nWhat do you want to sell?: ")
    if item_to_sell == "gold":
        print("You can't sell gold!")
        return
    if item_to_sell in inventory:
        amount = inventory[item_to_sell]
        del inventory[item_to_sell]
        if not "gold" in inventory:
            inventory["gold"] = 0
        gold = 100 * amount
        inventory["gold"] += gold
        print(f"You sold {item_to_sell} for {gold}!")


# Main program loop
while True:
    print("\n1. Open Treasure Box")
    print("2. Display Inventory")
    print("3. Sell item")
    print("4. Quit")
    
    choice = input("Choose an option: ")
    
    if choice == '1':
        open_treasure_box()
    elif choice == '2':
        display_inventory()
    elif choice == '3':
        sell_item()
    elif choice == '4':
        print("Goodbye, treasure hunter!")
        break
    else:
        print("Invalid choice. Try again.")
