# Gets around ciruclar dependencies
from enum import Enum
from typing import TYPE_CHECKING

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
    print(f"**{caster.name} casts {self.name}!")
    for effect in self.effects:
        for target in targets:
          effect.apply(caster, target)


def deal_damage(caster, target):
  damage = caster.agi
  target.take_damage(damage)


### Reusable spell effects

class SpellEffect:
    """Base class for spell effects."""
    def apply(self, caster, target):
        pass  # To be implemented by subclasses


class DealDamage(SpellEffect):
    """Damage effect with customizable bonus damage."""
    def __init__(self, bonus_damage=0, element=Elements.NONE):
        self.bonus_damage = bonus_damage
        self.element = element

    def apply(self, caster, target):
        damage = caster.agi + self.bonus_damage  # Agility-based damage
        target.take_damage(damage, self.element)



### SPELLS

all_spells = {
  "fireball" : Spell("Fireball 🔥", 10, [DealDamage(5, element=Elements.FIRE)]),
  "shock": Spell("Shock ⚡", num_targets=3, effects=[DealDamage(1, Elements.AIR)])
}