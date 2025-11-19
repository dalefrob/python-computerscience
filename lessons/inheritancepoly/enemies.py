import random

class Enemy:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
    
    def attack(self):
        print(f"{self.name} attacks for {self.attack_power + random.randint(1,5)}!")
    
    def take_damage(self, amount):
        self.hp -= amount
        print(f"{self.name} took {amount} damage!")

class Dragon(Enemy):
    def __init__(self, name, hp, attack_power, element):
        super().__init__(name, hp, attack_power)
        self.element = element
    
    def attack(self):
        print(f"{self.name} uses a {self.element} magic attack!")

    def take_damage(self, amount):
        super().take_damage(amount)
        print(f"{self.name} is angry!")

