from helpers import *

class BuffManager:
    def __init__(self, owner):
        self.owner = owner
        self.buffs = []

    def add_buff(self, buff):
        # dont add buff in certain circumstances
        if self.has_buff(buff.name) or self.owner.defeated:
            return
        
        buff.set_target(self.owner)
        buff.on_apply()
        self.buffs.append(buff)

    def remove_buff(self, buff):
        buff.on_expired()
        self.buffs.remove(buff)

    def new_turn(self):
        expired_buffs = []

        for buff in self.buffs:
            buff.on_new_turn()
            buff.turn_duration -= 1
            if buff.turn_duration <= 0:
                expired_buffs.append(buff)

        for buff in expired_buffs:
            self.remove_buff(buff)

    def clear_all(self):
        for buff in list(self.buffs):  # Copy to avoid modification during iteration
            self.remove_buff(buff)

    def has_buff(self, name):
        return any(buff.name == name for buff in self.buffs)

    def get_buffs_by_type(self, buff_type):
        return [buff for buff in self.buffs if isinstance(buff, buff_type)]  # OMG - this is sick.

    def __repr__(self):
        return f"<BuffManager: {len(self.buffs)} buffs on {self.owner.name}>"



class Buff():
    auto_inc = 0
    def __init__(self, name="noname buff", turn_duration=2):
        # set buff ID
        self.id = Buff.auto_inc
        Buff.auto_inc += 1

        self.name = name
        self.turn_duration = turn_duration

        self.target = None # set target after instantiation

    def set_target(self, target):
        self.target = target

    def on_apply(self):
        print(f"⚠️  {self.target.name} is afflicted by {self.name}.")

    def on_new_turn(self):
        pass

    def on_expired(self):
        print(f"{self.target.name} is no longer afflicted by {self.name}.")



class StatBuff(Buff):
    def __init__(self, name, turn_duration, stat_dict = None):
        super().__init__(name, turn_duration)
        if stat_dict is None:
            stat_dict = { "strength": 0, "agility": 0, "stamina": 0, "intellect": 0 }
        self.stat_dict = stat_dict


class DOTBuff(Buff):
    def __init__(self, name, turn_duration, damage_amount=1, element=Elements.NONE):
        super().__init__(name, turn_duration)
        self.damage_amount = damage_amount
        self.element = element
    
    def on_new_turn(self):
        print(f"{self.target.name} is hurt by {self.name}.")
        self.target.take_damage(self.damage_amount // self.turn_duration, self.element)


class SpellEffectBuff(Buff):
    def __init__(self, name, turn_duration, spell_effects):
        super().__init__(name, turn_duration)
        self.spell_effects = spell_effects or []


# ===== FACTORY ======


def make_rage():
    return StatBuff("Rage", 3, { "strength": 3 })


def make_burn():
    return DOTBuff("Burn", 3, 6, Elements.FIRE)

# ===== REGISTRY ======

buffs = {
    "burn": make_burn,
    "rage": make_rage
}