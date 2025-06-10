from g_signal import Signal
from spells import all_spells
from helpers import *
import random

class Bloke:
  def __init__(self, name):
    self.name = name
    # Stats
    self.strength = 4
    self.stamina = 5
    self.agility = 2
    self.intellect = 3
    # Atts
    self.max_health = self.stamina * 2.5
    self.hp = self.max_health
    # Spells
    self.spells = [all_spells["fireball"], all_spells["shock"], all_spells["cure"]]

    self.defeated = Signal()
    self.took_damage = Signal()
  

  def is_dead(self):
    return self.hp <= 0


  def get_damage(self):
    return self.strength + 2 # +2 as a stand in for weapon


  def get_spell(self):
    return random.choice(self.spells)


  def take_damage(self, amount, element=None):
    self.hp -= amount
    
    element_string = "" if not element else element + " "
    damage_string = colored(200, 0, 0, f"{amount} {element_string}damage!")
    print(f"{self.name} took {damage_string}")

    if self.hp <= 0:
      self.defeated.emit(self)


  def heal_damage(self, amount):
    self.hp += amount
    heal_string = colored(200, 200, 0, str(amount))
    print(f"{self.name} healed for {heal_string}.")
    if self.hp > self.max_health:
      self.hp = self.max_health


  def status(self):
    print(f"{self.name} is content.")
  

  def can_act(self):
    return not self.is_dead()


  def __str__(self):
    return f"{self.name}, str:{self.strength}, sta:{self.stamina}, agi:{self.agility}"

