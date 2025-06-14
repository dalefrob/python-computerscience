# Gets around ciruclar dependencies
import random
from helpers import *
from buff import buffs
from copy import copy


class Spell():
  def __init__(self, name, num_targets = 1, effects = []):
    self.name = name
    self.num_targets = num_targets
    self.effects = effects
  
  def cast(self, caster, targets):
    cast_string = colored(YELLOW, f"**{caster.name} casts {self.name}!")
    print(cast_string)
    for target in targets:
        for effect in self.effects:
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


class ApplyBuff(SpellEffect):
    def __init__(self, buff, apply_to_self=False):
        super().__init__()
        self.buff = buff
        self.apply_to_self = apply_to_self
    
    def apply(self, caster, target):
        receiver = caster if self.apply_to_self else target
        apply_chance = getattr(self.buff, "apply_chance", 1.0)
        should_apply = random.random() < apply_chance
        if should_apply:
            copied_buff = copy(self.buff)
            receiver.buff_manager.add_buff(copied_buff)


class HealDamage(SpellEffect):
    """Healing self."""
    def __init__(self, healing_amount=10):
        self.healing_amount = healing_amount

    def apply(self, caster, target):
        caster.heal_damage(self.healing_amount)


# ==== SPELL FACTORIES ====

def make_doomsday(caster):
    damage = 15 + caster.intellect // 2
    return Spell("Doomsday ☄️", num_targets=4, effects=[DealDamage(damage, element=Elements.EARTH)])

def make_fireball(caster):
    damage = 8 + caster.intellect // 2
    return Spell("Fireball 🔥", effects=[DealDamage(damage, element=Elements.FIRE), ApplyBuff(buffs["burn"](), False)])

def make_shock(caster):
    max_damage = 4 + caster.intellect // 2
    return Spell("Shock ⚡", num_targets=3, effects=[DealDamage(roll_damage=(1, max_damage), element=Elements.AIR), ApplyBuff(buffs["paralysis"]())])

def make_cure(caster):
    return Spell("Cure 🩹", effects=[HealDamage(5), ApplyBuff(buffs["regen"](), True)])

def make_curaga(caster):
    return Spell("Curaga 💊", effects=[HealDamage(20)])

# ==== SPELL REGISTRY ====

all_spells = {
    "doomsday": make_doomsday,
    "fireball": make_fireball,
    "shock": make_shock,
    "cure": make_cure,
    "curaga": make_curaga,
}
