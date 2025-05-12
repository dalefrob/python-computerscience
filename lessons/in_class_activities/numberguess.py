import random

MAXNUM = 100

# Choose a rand num
rand_num = random.randint(0, MAXNUM)
number_of_guesses = 0

# Take a guess
player_guess = -1

# Loop while the guess is wrong
while player_guess != rand_num:
    player_guess = int( input(f"Guess a number between 0 and {MAXNUM}. \nYour guess: ") )
    # number_of_guesses = number_of_guesses + 1
    number_of_guesses += 1
    # Check if its higher or lower
    if player_guess > rand_num:
        print("Too high!")
    elif player_guess < rand_num:
        print("Too low!")

print(f"You got it! That took {number_of_guesses} guesses!")
