# Lesson Objective: Create a simple rock-paper-scissors game in Python.
# Programming Concepts: Functions, Conditionals, Loops, Randomness
# Libraries: random

from random import choice

moves = ["rock", "paper", "scissors"]

def check(move, cpu_choice):
    if move == cpu_choice:
        print("Draw!")
    elif (move == "rock" and cpu_choice == "scissors") or \
         (move == "paper" and cpu_choice == "rock") or \
         (move == "scissors" and cpu_choice == "paper"):
        print("You win!")
    else:
        print("You lose!")
    play()

print("Welcome to Janken")

def play():
    move = input("rock, paper, or scissors, exit?: ")
    if move == "exit":
        print("Goodbye!")
        return
    if move in moves:
        cpu_choice = choice(moves)
        print(cpu_choice)
        check(move, cpu_choice)
    else:
        print("Play properly! :(")
        play()

play()


# def main():
#     pass

# if __name__ == "__main__":
#     main()