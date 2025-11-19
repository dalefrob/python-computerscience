
validinput = False

while validinput == False:
    try: 
        string_age = input("What is your age?")
        age = int(string_age)
        validinput = True
    except:
        print("Enter a valid number")

if age > 70:
    print("Maybe you shouldn't drive at yur age")
elif age >= 18:
    haslicence = input("Do you have a licence? Y/N? ").upper()
    if haslicence == "Y":
        print("You can drive")
    else:
        print("Go and get a licence")
else:
    print("You have to walk")