import random
import time

def sort_array(arr):
    """
    Sorts an array using the bubble sort algorithm.
    The algorithm repeatedly steps through the list, compares adjacent elements,
    and swaps them if they are in the wrong order.
    The pass through the list is repeated until the list is sorted.
    """
    # Outer loop to iterate through the entire array
    for i in range(len(arr)):
        # Calculate the range limit before the inner loop
        range_limit = len(arr) - i - 1
        
        # Inner loop to compare adjacent elements
        for j in range(0, range_limit):
            # Compare the current element with the next element
            current_element = arr[j]
            next_element = arr[j + 1]
            
            # Check if the current element is greater than the next element
            if current_element > next_element:
                # Swap the elements
                temp = current_element
                arr[j] = next_element
                arr[j + 1] = temp
        
    # Return the sorted array
    return arr


if __name__ == "__main__":
    # Generate a large random array
    unsorted_array = [random.randint(0, 10000) for _ in range(1000)]    
    # Start timing
    start_time = time.time()

    # Run the sorting algorithm
    sort_array(unsorted_array)

    # End timing
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time
    print(f"Bubble sort took {duration:.6f} seconds.")