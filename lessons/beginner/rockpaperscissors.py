import random

points = 0

while True:
    playerchoice = input("(R)ock, (P)aper, or (S)cissors? (Q)uit:").capitalize()
    computerchoice = random.choice("PSR")

    if playerchoice == "Q":
        break

    print(f"Player:{playerchoice} CPU:{computerchoice}")

    if playerchoice == computerchoice:
        print("DRAW")
    else:
        if playerchoice == "R" and computerchoice == "S" or playerchoice == "S" and computerchoice == "P" or \
            playerchoice == "P" and computerchoice == "R":
            print("PLAYER WINS")
            points += 1
        else:
            print("CPU WINS")

print(f"Points: {points}")