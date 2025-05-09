import random

# List of Magic 8-Ball responses
responses = [
    "It is certain.",
    "Without a doubt.",
    "Yes, definitely.",
    "You may rely on it.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."
]

print("🔮 Welcome to the Magic 8-Ball Simulator!")
print("Ask me any 'Yes or No' question, and I will predict your fate.")
print("Type 'exit' to leave the game.\n")

while True:
    question = input("What is your question? ")
    
    if question.lower() == "exit":
        print("Goodbye, and may your future be bright!")
        break
    
    if question.strip() == "":
        print("You need to ask something!")
    else:
        # Randomly select a response from the list
        answer = random.choice(responses)
        print("🔮 Magic 8-Ball says: " + answer)
