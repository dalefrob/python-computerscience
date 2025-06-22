import os

# Get the full path of the current file
file_path = os.path.abspath(__file__)

# Get the folder (directory) that contains this file
file_directory = os.path.dirname(file_path)

newfiles_directory = file_directory + "/texts"

if not os.path.exists(file_directory + "/texts"):
    os.makedirs(newfiles_directory)

with open(f"{newfiles_directory}/myfile.txt", "w") as file:
    file.write("I wrote to a file! Ner ner! \n")
    file.write("New line bro. \n")

with open(f"{newfiles_directory}/myfile.txt", "a") as file:
    message = "This is some bytecode!! \n".encode("utf-8")
    h_message = message.hex()
    file.write(h_message)