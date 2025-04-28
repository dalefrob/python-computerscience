class Animal:
    def __init__(self, breed, name):
        self.breed = breed
        self.name = name
    
    def say(self):
        print(f"{self.name}, the {self.breed} makes a noise")