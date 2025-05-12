import random
# Magic 8 Ball

answers = [
    "Yes, absolutely!  🔮🔮",    # index 0 --- answers[0]
    "Lucky!",   # 1
    "Not going to happen!",   # 2
    "No way! 💀💀"   # 3
]

index = random.randint(0, len(answers) - 1)

# Ask the user to ask a question.. input
# Then give them a random answer.  answers[random_index]
# Loop the question asking if you can. while