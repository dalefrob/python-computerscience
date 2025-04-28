import random
from animal import *

names = ["Ness", "Lucas", "John"]
animals = ["Cat", "Dog", "Mouse"]

def main():
    rnd_animal = random.randint(0, len(animals) - 1)
    rnd_name = random.randint(0, len(names) - 1)

    cat = Animal(animals[rnd_animal], names[rnd_name])
    cat.say()


if __name__ == '__main__':
    main()