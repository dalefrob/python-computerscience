class Dog:
    def __init__(self, name):
        self.name = name
        self.last_eaten_food = ""
    
    def bark(self):
        print(f"Woof! My name is {self.name}")
    
    def feed(self, food):
        print(f"Yum! {self.name} eats {food}")
        self.last_eaten_food = food

dog1 = Dog("Spot")
dog2 = Dog("Sparky")

dogs = [dog1, dog2]

for o in dogs:
    o.bark()
    o.feed("chicken bones")

print(dog1.last_eaten_food)