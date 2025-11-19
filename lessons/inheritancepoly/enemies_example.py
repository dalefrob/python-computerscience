# BASE CLASS
class Enemy:
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power

    def attack(self):
        print(f"{self.name} attacks for {self.attack_power} damage!")

    def take_damage(self, amount):
        self.hp -= amount
        print(f"{self.name} takes {amount} damage! HP left: {self.hp}")

# CHILD CLASSES
class Goblin(Enemy):
    def attack(self):
        print(f"{self.name} slashes with a rusty dagger for {self.attack_power} damage!")

class Skeleton(Enemy):
    def attack(self):
        print(f"{self.name} shoots and arrow for {self.attack_power} damage!")

class Dragon(Enemy):
    def __init__(self, name, hp, attack_power, color):
        super().__init__(name, hp, attack_power)
        self.color = color

    def attack(self):
        print(f"{self.name}, the {self.color} dragon breathes FIRE for {self.attack_power} damage!")
