import random

def binary_search(arr, target):
    left = 0
    right = len(arr) - 1 
    mid = (left + right) // 2
    while left <= right:
        mid = (left + right) // 2  # Double slash is for floor division
        if arr[mid] == target:
            return True
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return False

sorted_list = []
n = 0
for i in range(100):
    n += random.randint(0, 5)
    sorted_list.append(n)
    

search_target = input("Enter a number to search: ")

# Show the sorted list
print(sorted_list)

result_found = binary_search(sorted_list, int(search_target))
if result_found:
    print(f"Element ({search_target}) found")
else:
    print(f"Element ({search_target}) not found")