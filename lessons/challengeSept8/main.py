lettertable = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    "i": 9,
    "j": 10,
    "k": 11,
    "l": 12,
    "m": 13,
    "n": 14,
    "o": 15,
    "p": 16,
    "q": 17,
    "r": 18,
    "s": 19,
    "t": 20,
    "u": 21,
    "v": 22,
    "w": 23,
    "x": 24,
    "y": 25,
    "z": 26,
}

#1 get the word to count from the user 
# 2 give double points to double letters

def countwordvalue(word : str):
    total = 0
    previous = ""
    for character in word:
        if previous == character:
            total += lettertable[character] * 2
        else:
            total += lettertable[character]
        previous = character
    return total

word = input("Enter a word:")

result = countwordvalue(word)
print(f"{word} = {result}")