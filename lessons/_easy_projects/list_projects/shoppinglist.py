shopping_list = []

def display_menu():
    print("\n📝 Shopping List Menu:")
    print("1. Add an item")
    print("2. Remove an item")
    print("3. View the list")
    print("4. Clear the list")
    print("5. Exit")

def add_item():
    item = input("Enter an item to add: ")
    shopping_list.append(item)
    print(f"'{item}' has been added to the list.")

def remove_item():
    item = input("Enter an item to remove: ")
    if item in shopping_list:
        shopping_list.remove(item)
        print(f"'{item}' has been removed from the list.")
    else:
        print(f"'{item}' not found in the list.")

def view_list():
    print("\nCurrent Shopping List:")
    for idx, item in enumerate(shopping_list, start=1):
        print(f"{idx}. {item}")
    if not shopping_list:
        print("The list is empty.")

def clear_list():
    shopping_list.clear()
    print("The shopping list has been cleared.")

while True:
    display_menu()
    choice = input("Choose an option: ")
    
    if choice == "1":
        add_item()
    elif choice == "2":
        remove_item()
    elif choice == "3":
        view_list()
    elif choice == "4":
        clear_list()
    elif choice == "5":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, please try again.")
