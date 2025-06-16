import random

# List of possible words
words = ["string"]

# with open("words.txt", "r") as file:
#     line = file.readline()
#     while line:
#         # Process the line here
#         words.append(line.strip())  # Remove trailing newline character
#         line = file.readline()

# Randomly select a word
secret_word = random.choice(words)

# Create a list to represent the hidden word (e.g., "_ _ _")
hidden_word = ["_"] * len(secret_word)

# List to keep track of guessed letters
guessed_letters = []

print("Welcome to the Word Guessing Game!")
print("Try to guess the word, one letter at a time.")

def display_word():
    # This just prints out the current state of the word
    print("Word: " + " ".join(hidden_word))

def guess_letter():
    letter = input("Guess a letter: ").lower()

    if letter == secret_word:
        for i, char in enumerate(secret_word):
            hidden_word[i] = char
    elif letter in guessed_letters:
        print(f"You already guessed '{letter}'. Try again.")
    elif len(letter) != 1 or not letter.isalpha():
        print("Please enter a single valid letter.")
    else:
        guessed_letters.append(letter)
        if letter in secret_word:
            print(f"Good guess! '{letter}' is in the word.")
            # Loop through the indexes of the secret word
            index = 0
            while index < len(secret_word):
                if secret_word[index] == letter:
                    hidden_word[index] = letter
                index += 1
        else:
            print(f"Sorry, '{letter}' is not in the word.")

# Game loop
while "_" in hidden_word:
    display_word()
    guess_letter()

print("\n🎉 Congratulations! You've guessed the word: " + secret_word)
