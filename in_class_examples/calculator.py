print("Hello World")

a = input("Enter the first number")
b = input("Enter the second number")
operation = input("Enter the operation")  # + - * /

answer = 0

if operation == "+":
    answer = int(a) + int(b)
elif operation == "-":    # elif is else + if
    pass
else:
    print("thats not an operation")    

# Show the answer
print(answer)