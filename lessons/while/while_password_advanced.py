password = "gumtree"
guess = ""
attempts = 5
access = False
while(attempts > 0):
    guess = input("What's the password?: ")
    if (guess == password):
        access = True
        break
    attempts = attempts - 1

if (access == True):
    print("Access Granted.")
else:
    print("Access Denied.")