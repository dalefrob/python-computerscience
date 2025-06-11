from g_signal import Signal
from buff import *
from spells import all_spells
from helpers import *
import random


class Bloke:
    def __init__(self, name):
        self.name = name
        self.buff_manager = BuffManager(self)
        # Stats
        self.strength = random.randint(2,5)
        self.stamina = random.randint(2,5)
        self.agility = random.randint(2,5)
        self.intellect = random.randint(2,5)
        # Atts
        self.max_health = 10 + (self.stamina * 3)
        self.hp = self.max_health
        # Spells
        self.spells = [all_spells["fireball"]
                       (), all_spells["shock"](), all_spells["cure"]()]
        
        self.defeated = False
        self.on_defeated = Signal()


    def new_turn(self):
        self.buff_manager.new_turn()

    def get_damage(self):
        return self.strength + 2  # +2 as a stand in for weapon

    def get_spell(self):
        return random.choice(self.spells)

    def take_damage(self, amount, element=None):
        self.hp -= amount

        element_string = "" if not element else element + " "
        damage_string = colored(200, 0, 0, f"{amount} {element_string}damage!")
        print(f"{self.name} took {damage_string}")

        if self.hp <= 0:
            self.defeated = True
            self.on_defeated.emit(self)

    def heal_damage(self, amount):
        self.hp += amount
        heal_string = colored(0, 200, 0, str(amount))
        print(f"{self.name} healed for {heal_string}.")
        if self.hp > self.max_health:
            self.hp = self.max_health

    def status(self):
        print(f"{self.name} is content.")

    def can_act(self):
        return not self.defeated

    def __str__(self):
        return f"{self.name}, Strength:{self.strength}, Agility:{self.agility}, Intellect:{self.intellect}, Stamina:{self.stamina}, HP:{self.hp}"
