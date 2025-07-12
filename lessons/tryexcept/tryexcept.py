# test for exceptions and handle them
while True:
  myinput = input("Enter two numbers separated by a space")
  try:
    stripped = myinput.strip()
    num1, num2 = stripped.split(" ")
    print(f"You entered numbers {num1} and {num2}.")
    break # < ---- break exits the while loop
  except:
    print("Invalid input!")
  finally:
    print("Out of the try except block")

# raise your own exceptions
age = input("Enter your age: ")

if int(age) <= 0:
  raise Exception("Sorry, you must have been born first.")

print("Does the program get here?")