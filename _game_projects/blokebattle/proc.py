import random
from helpers import *
from spells import *
from buff import *

class ProcContext:
    """
    Send anything stateful via this data class to trigger effects
    """
    def __init__(self, owner = None, target = None):
        self.owner = owner
        self.target = target


class Proc():
    def __init__(self, proc_timing=ProcTiming.ON_HIT, trigger_chance=0.5):
        self.source = None
        self.proc_timing = proc_timing
        self.trigger_chance = trigger_chance

    @property
    def name(self):
        return self.source.name or "Unnamed Proc"

    def set_source(self, source):
        self.source = source

    def should_trigger(self):
        return random.random() < self.trigger_chance

    def trigger(self, context : ProcContext):
        pass


class AddMultDamage(Proc):
    def __init__(self, proc_timing, trigger_chance, damage_multiplier, element):
        super().__init__(proc_timing, trigger_chance)
        self.damage_multiplier = damage_multiplier
        self.element = element
    
    def trigger(self, context : ProcContext):
        print(colored_by_value(255, 190, 0 ,f"Item Proc! {self.source.name}-->Additional Damage"))
        dmg = round(context.owner.item.get_damage() * self.damage_multiplier)
        context.target.take_damage(dmg)


class HealOnHitProc(Proc):
    def __init__(self, proc_timing, trigger_chance, heal_amount):
        super().__init__(proc_timing, trigger_chance)
        self.heal_amount = heal_amount

    def trigger(self, context: ProcContext):
        print(colored_by_value(255, 190, 0 ,f"Item Proc! {self.source.name}-->Life Leech"))
        context.owner.heal_damage(self.heal_amount)


class EffectProc(Proc):
    def __init__(self, proc_timing, trigger_chance, effect):
        super().__init__(proc_timing, trigger_chance)
        self.effect = effect
    
    def trigger(self, context : ProcContext):
        print(colored_by_value(255, 190, 0 ,f"Item Proc! {self.source.name}"))
        self.effect.apply(context.owner, context.target)


class CastBuffProc(Proc):
    def __init__(self, proc_timing, trigger_chance, buff, cast_on_self=False):
        super().__init__(proc_timing, trigger_chance)
        self.buff = buff
        self.cast_on_self = cast_on_self
    
    def trigger(self, context : ProcContext):
        receiver = context.owner if self.cast_on_self else context.target
        apply_chance = getattr(self.buff, "apply_chance", 1.0)
        should_apply = random.random() < apply_chance
        if should_apply:
            copied_buff = copy(self.buff)
            receiver.buff_manager.add_buff(copied_buff)