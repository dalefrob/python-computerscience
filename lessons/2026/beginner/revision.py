name = "Roberts"
length = 7

for i in range(length):
    print(name[i])

def sayHello(to_name):
    print("Hello " + to_name)

sayHello("Justin")
sayHello("Tobby")
sayHello(name)

def add(a, b):
    answer = a + b
    return answer

totalage = add(12, 7)
print(totalage)