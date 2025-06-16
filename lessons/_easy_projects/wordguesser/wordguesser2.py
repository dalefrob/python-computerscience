import random

wordlist = ["apple", "banana", "strawberry"]

tries = 0
MAXTRIES = 5

correctWord = random.choice(wordlist)
hiddenWord = ["_"] * len(correctWord)
joinedWord = " ".join(hiddenWord)

while tries < MAXTRIES: # loop to keep asking the player
    guessed_letter = input(f"Guess a letter ({MAXTRIES - tries} tries left): ")
    if guessed_letter == correctWord:
        print("You got it!")
        break

    if guessed_letter in correctWord:
        print(guessed_letter, "is in the word")
    else:
        print(guessed_letter, "is not in the word")
    
    tries += 1