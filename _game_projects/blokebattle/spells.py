# Gets around ciruclar dependencies
from enum import Enum
import random
from typing import TYPE_CHECKING
from helpers import *

if TYPE_CHECKING:
  from bloke import *

class Elements(str, Enum):
   NONE = None
   FIRE = "Fire"
   WATER = "Water"
   EARTH = "Earth"
   AIR = "Air"


class Spell():
  def __init__(self, name, num_targets = 1, effects = []):
    self.name = name
    self.num_targets = num_targets
    self.effects = effects
  
  def cast(self, caster, targets):
    cast_string = colored(200, 200, 0, f"**{caster.name} casts {self.name}!")
    print(cast_string)
    for effect in self.effects:
        for target in targets:
          effect.apply(caster, target)


def deal_damage(caster, target):
  damage = caster.agi
  target.take_damage(damage)


### Reusable spell effects

class SpellEffect():
    """Base class for spell effects."""
    def apply(self, caster, target):
        pass  # To be implemented by subclasses


class DealDamage(SpellEffect):
    """Damage effect with customizable bonus damage."""
    def __init__(self, base_damage=0, roll_damage=(1,1), element=Elements.NONE):
        self.base_damage = base_damage
        self.roll_damage = roll_damage
        self.element = element

    def apply(self, caster, target):
        min, max = self.roll_damage
        damage = (caster.intellect // 2) + self.base_damage + random.randint(min, max) # Agility-based damage
        target.take_damage(damage, self.element)

class HealDamage(SpellEffect):
    """Healing self."""
    def __init__(self, healing_amount=10):
        self.healing_amount = healing_amount

    def apply(self, caster, target):
        caster.heal_damage(self.healing_amount)


### SPELLS

all_spells = {
  "fireball" : Spell("Fireball 🔥", effects=[DealDamage(8, element=Elements.FIRE)]),
  "shock": Spell("Shock ⚡", num_targets=3, effects=[DealDamage(roll_damage=(1,6), element=Elements.AIR)]),
  "cure": Spell("Cure 🩹", effects=[HealDamage(10)])
}