from g_signal import Signal
from spells import all_spells
import random

class Bloke:
  def __init__(self, name):
    self.name = name
    # Stats
    self.str = 4
    self.stam = 5
    self.agi = 2
    # Atts
    self.hp = self.stam * 2.5
    # Spells
    self.spells = [all_spells["fireball"], all_spells["shock"]]

    self.defeated = Signal()
    self.took_damage = Signal()
  

  def is_dead(self):
    return self.hp <= 0


  def get_damage(self):
    return self.str


  def get_spell(self):
    return random.choice(self.spells)


  def take_damage(self, amount, element=None):
    self.hp -= amount
    self.took_damage.emit(self, amount, element)
    if self.hp <= 0:
      self.defeated.emit(self)


  def status(self):
    print(f"{self.name} is content.")
  

  def can_act(self):
    return not self.is_dead()


  def __str__(self):
    return f"{self.name}, str:{self.str}, sta:{self.stam}, agi:{self.agi}"

