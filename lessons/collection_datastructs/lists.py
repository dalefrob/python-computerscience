# Introduction to Python Lists

# Creating a list
fruits = ["apple", "banana", "cherry"]
print("Fruits:", fruits)

# Accessing elements
print("First fruit:", fruits[0])  # Indexing starts at 0
print("Last fruit:", fruits[-1])  # Negative indexing

# Modifying elements
fruits[1] = "blueberry"
print("Modified fruits:", fruits)

# Adding elements
fruits.append("orange")  # Adds to the end
print("After append:", fruits)

fruits.insert(1, "kiwi")  # Inserts at a specific position
print("After insert:", fruits)

# Removing elements
fruits.remove("cherry")  # Removes by value
print("After remove:", fruits)

popped_fruit = fruits.pop()  # Removes the last element
print("Popped fruit:", popped_fruit)
print("After pop:", fruits)

# Slicing a list
print("Sliced list (first two):", fruits[:2])

# Iterating through a list
print("Iterating through the list:")
for fruit in fruits:
  print(fruit)

# Checking membership
print("Is 'apple' in the list?", "apple" in fruits)

# List length
print("Number of fruits:", len(fruits))

# Sorting a list
fruits.sort()
print("Sorted fruits:", fruits)

# Reversing a list
fruits.reverse()
print("Reversed fruits:", fruits)

# Copying a list
fruits_copy = fruits.copy()
print("Copied list:", fruits_copy)

# Nested lists
nested_list = [["apple", "banana"], ["carrot", "potato"]]
print("Nested list:", nested_list)
print("Accessing nested list element:", nested_list[1][0])

# List comprehension
squares = [x**2 for x in range(10)]
print("List comprehension (squares):", squares)

upperfruits = [x.upper() for x in fruits]
print("List comprehension (upperfruits):", upperfruits)

lessfivelist = [x for x in range(10) if x < 5]
print("List comprehension (newlist):", lessfivelist)