import random
from selectionsort import selection_sort
from bubblesort import sort_array
import time

unsorted_array = [random.randint(0, 10000) for _ in range(1000)]


start_time = time.time()
sort_array(unsorted_array.copy()) 
end_time = time.time()
duration = end_time - start_time
print(f"Compare - Bubble sort took {duration:.6f} seconds.")

start_time = time.time()
selection_sort(unsorted_array.copy())
end_time = time.time()
duration = end_time - start_time
print(f"Compare - Selection sort took {duration:.6f} seconds.")