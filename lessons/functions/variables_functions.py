# Potion Maker Simulator - Beginner Python Lesson

# --- Variable Types ---
# Let's define some potion ingredients and potion properties
potion_name = "Invisibility"
ingredient_count = 3
is_glowing = True

print("Potion name:", potion_name)
print("Number of ingredients:", ingredient_count)
print("Is the potion glowing?", is_glowing)

print("\n---")

# --- Function with Arguments and Return Value ---
def brew_potion(name, ingredient_count):
    return f"The potion '{name}' needs {ingredient_count} magical ingredients!"

# Example call to the function
message = brew_potion("Levitation", 4)
print(message)

print("\n---")

# --- Challenge Function: Add a safety check ---
def magic_effect(name, power_level, is_safe):
    if is_safe:
        return f"The '{name}' potion (Power Level: {power_level}) is safe to use!"
    else:
        return f"Warning! The '{name}' potion (Power Level: {power_level}) is TOO DANGEROUS!"

# Test the function
print(magic_effect("Firestorm", 9, False))
print(magic_effect("Healing Light", 3, True))

print("\n---")

# --- Optional Challenge: Make your own potion function below ---
# Example template:
# def my_potion(name, ...):
#     return ...
