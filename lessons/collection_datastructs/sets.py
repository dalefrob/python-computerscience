# Demonstrating features of Python sets

# Creating sets
set1 = {1, 2, 3, 4, 5}
set2 = {4, 5, 6, 7, 8}

print("Set 1:", set1)
print("Set 2:", set2)

# Adding elements to a set
set1.add(6)
print("\nAfter adding 6 to Set 1:", set1)

# Removing elements from a set
set1.remove(3)
print("After removing 3 from Set 1:", set1)

# Checking membership
print("\nIs 4 in Set 1?", 4 in set1)
print("Is 10 in Set 2?", 10 in set2)

# Set operations
union_set = set1.union(set2)
print("\nUnion of Set 1 and Set 2:", union_set)

intersection_set = set1.intersection(set2)
print("Intersection of Set 1 and Set 2:", intersection_set)

difference_set = set1.difference(set2)
print("Difference of Set 1 and Set 2 (Set 1 - Set 2):", difference_set)

symmetric_difference_set = set1.symmetric_difference(set2)
print("Symmetric Difference of Set 1 and Set 2:", symmetric_difference_set)

# Checking subset and superset
subset = {4, 5}
print("\nIs", subset, "a subset of Set 1?", subset.issubset(set1))
print("Is Set 1 a superset of", subset, "?", set1.issuperset(subset))

# Clearing a set
set1.clear()
print("\nAfter clearing Set 1:", set1)