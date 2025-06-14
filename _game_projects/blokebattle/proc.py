import random
from helpers import *
from spells import *
from buff import *

class Proc():
    def __init__(self, proc_timing=ProcTiming.ON_HIT, trigger_chance=0.5):
        self.source = None
        self.proc_timing = proc_timing
        self.trigger_chance = trigger_chance

    def set_source(self, source):
        self.source = source

    def should_trigger(self):
        return random.random() < self.trigger_chance

    def trigger(self, attacker, target, context):
        pass


class AddMultDamage(Proc):
    def __init__(self, proc_timing, trigger_chance, damage_multiplier, element):
        super().__init__(proc_timing, trigger_chance)
        self.damage_multiplier = damage_multiplier
        self.element = element
    
    def trigger(self, attacker, target, context):
        print(colored_by_value(255, 190, 0 ,f"Item Proc: Damage x{self.damage_multiplier}"))
        dmg = attacker.item.get_damage()
        return { "extra_damage": dmg * self.damage_multiplier, "element": self.element }


class CastSpellProc(Proc):
    def __init__(self, proc_timing, trigger_chance, spell):
        super().__init__(proc_timing, trigger_chance)
        self.spell = spell
    
    def trigger(self, attacker, target, context):
        self.spell.cast(attacker, target)


class CastBuffProc(Proc):
    def __init__(self, proc_timing, trigger_chance, buff, cast_on_self=False):
        super().__init__(proc_timing, trigger_chance)
        self.buff = buff
        self.cast_on_self = cast_on_self
    
    def trigger(self, attacker, target, context):
        receiver = attacker if self.cast_on_self else target
        apply_chance = getattr(self.buff, "apply_chance", 1.0)
        should_apply = random.random() < apply_chance
        if should_apply:
            copied_buff = copy(self.buff)
            receiver.buff_manager.add_buff(copied_buff)