import random

wordlist = ["orange", "crocodile", "quadratic"]
answer = random.choice(wordlist)
hiddenword = ["_"] * len(answer)

print(hiddenword)
guess = input("Guess a letter: ")

if guess in answer:
    for position, letter in enumerate(answer):
        if letter == guess:
            print(f"Found {letter} at {position}")

            hiddenword[position] = letter
            print(hiddenword)
else:
    print("Try again!")