import os

# Get the full path of the current file
file_path = os.path.abspath(__file__)

# Get the folder (directory) that contains this file
file_directory = os.path.dirname(file_path)

print("This file is located in:", file_directory)