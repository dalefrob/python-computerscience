import random
from rich import print
from rich.prompt import Prompt

# Make sure all projects load a word ---
# Show students 
# how to install new modules
# how to load words from a text file

wordlist = ["apple", "banana", "strawberry"]

mistakes = 0
MAX_MISTAKES = 5

correctWord = random.choice(wordlist)
hiddenWord = ["_"] * len(correctWord)
guessed_letters = []

got_word = False

def show_hiddenword():
    for index, letter in enumerate(correctWord):
        if letter in guessed_letters:
            hiddenWord[index] = letter
    print(" ".join(hiddenWord))

print("[yellow]Welcome to the Word Guesser Game![/yellow]")

while True: # loop to keep asking the player
    show_hiddenword()
    if not "_" in hiddenWord:
        got_word = True
        break

    guess = Prompt.ask(f"[blue]Guess a letter[/blue], or the whole word. ({MAX_MISTAKES - mistakes} mistakes left): ")
    if guess == correctWord:
        got_word = True
        break
    
    if guess in guessed_letters:
        print(f"You already guessed {guess}")
    elif guess in correctWord:
        print(guess, "is in the word")
    else:
        print(guess, "is not in the word")
        mistakes += 1
    guessed_letters.append(guess)

    if mistakes >= MAX_MISTAKES:
        break
    
if got_word:
    print(f"[cyan]You got it with {mistakes} mistakes![/cyan]")
else:
    print(f"[red]No tries left! Better luck next time.[/red]")
print(f"The word was '{correctWord}'")