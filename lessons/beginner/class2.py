
names = ["Pikachu"]
names.append("Dale")
names.append("Justin")
names.append("Rayquaza")

index = names.index("Justin")
names[index] = "Super Justin"

for name in names:
    print(name)

for i in range(3):
    row = ""
    for j in range(3):
        row += "[]"
    print(row)