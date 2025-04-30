import time
import random

def selection_sort(arr):
    """
    Sorts an array using the selection sort algorithm.
    The algorithm divides the array into two parts: sorted and unsorted.
    It repeatedly selects the smallest element from the unsorted part and moves it to the end of the sorted part.
    """
    # Loop through each element in the array
    for i in range(len(arr)):
        # Assume the current index is the minimum
        min_index = i

        # Find the smallest element in the unsorted part of the array
        for j in range(i + 1, len(arr)):
            current_element = arr[j]
            smallest_element = arr[min_index]
            if current_element < smallest_element:
                # Update min_index if a smaller element is found
                min_index = j

        # Swap the smallest element found with the first element of the unsorted part
        first_unsorted_element = arr[i]
        smallest_element = arr[min_index]
        arr[i], arr[min_index] = smallest_element, first_unsorted_element

    # Return the sorted array
    return arr


if __name__ == "__main__":
    # Generate a large random array
    unsorted_array = [random.randint(0, 10000) for _ in range(1000)]

    # Copy the array to preserve the original for multiple tests
    array_to_sort = unsorted_array.copy()

    # Start timing
    start_time = time.time()

    # Run the sorting algorithm
    selection_sort(array_to_sort)

    # End timing
    end_time = time.time()

    # Calculate duration
    duration = end_time - start_time
    print(f"Selection sort took {duration:.6f} seconds.")
