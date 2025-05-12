for i in range(100):
    print(i)

name = "ninetales"
for char in name:
    print(char)




guess = ""
answer = "ninetales"
while guess != answer:
    guess = input("Guess my favorite pokemon!: ")
    if guess != answer:
        print("wrong!")

print("You got it!")