"""This is a multiline comment.

Use it to describe what the overall code does.
"""

# Python supports static typing!
# Defining a function that takes in two parameters and returns a formatted string.
def greet(name : str, quest : str) -> str:
    response = f"Pleased to meet you, {name}! Good luck on your quest to {quest}!"
    return response

# Asking for input
name = input("What is your name?")
quest = input("What is your quest?")

# Calling the function and putting the returned value in a variable
response = greet(name, quest)

# Printing the value using a built-in function
print(response)