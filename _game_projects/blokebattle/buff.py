from helpers import *
from enum import IntFlag, auto


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
            buff.turn_duration -= 1
            if buff.turn_duration <= 0:
                expired_buffs.append(buff)
            else:
                buff.on_new_turn()

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
    def __init__(self, name="noname buff", turn_duration=2, apply_chance=1.0, is_debuff=False):
        # set buff ID
        self.id = Buff.auto_inc
        Buff.auto_inc += 1

        self.name = name
        self.turn_duration = turn_duration + 1
        self.apply_chance = apply_chance
        self.is_debuff = is_debuff

        self.target = None # set target after instantiation

    def set_target(self, target):
        self.target = target

    def on_apply(self):
        if self.is_debuff:
            print(f"⚠️  {self.target.name} is afflicted by {self.name}.")
        else:
            print(f"💠  {self.target.name} gained {self.name}.")

    def on_new_turn(self):
        pass

    def on_expired(self):
        if self.is_debuff:
            print(f"✔️  {self.target.name} is no longer afflicted by {self.name}.")
        else:
            print(f"🔶  {self.target.name} lost {self.name}.")


class StatBuff(Buff):
    def __init__(self, name, turn_duration, stat_dict, is_debuff = False):
        super().__init__(name, turn_duration, is_debuff=is_debuff)
        self.stat_dict = stat_dict or {}

    def on_apply(self):
        super().on_apply()
        for stat, delta in self.stat_dict.items():
            if delta != 0:
                print(f"📈 {self.target.name}'s {stat} changed by {delta}.")

    def on_expired(self):
        for stat, delta in self.stat_dict.items():
            if delta != 0:
                print(f"📉 {self.target.name}'s {stat} change of {delta} expired.")


class BonusStatBuff(Buff):
    def __init__(self, name, turn_duration, bonus_stat_dict, is_debuff = False):
        super().__init__(name, turn_duration, is_debuff=is_debuff)
        self.bonus_stat_dict = bonus_stat_dict or {}

    def on_apply(self):
        super().on_apply()
        for stat, delta in self.bonus_stat_dict.items():
            if delta != 0:
                print(f"📈 {self.target.name}'s {stat} changed by {delta}.")

    def on_expired(self):
        for stat, delta in self.bonus_stat_dict.items():
            if delta != 0:
                print(f"📉 {self.target.name}'s {stat} change of {delta} expired.")


class DOTBuff(Buff):
    def __init__(self, name, turn_duration, apply_chance, damage_amount=1, element=Elements.NONE):
        super().__init__(name, turn_duration, apply_chance, True)
        self.initial_turn_duration = turn_duration
        self.damage_amount = damage_amount
        self.element = element
    
    def on_new_turn(self):
        print(f"{self.target.name} is hurt by {self.name}.")
        self.target.take_damage(self.damage_amount // self.initial_turn_duration, self.element)


class HOTBuff(Buff):
    def __init__(self, name, turn_duration, apply_chance, heal_amount=1):
        super().__init__(name, turn_duration, apply_chance)
        self.initial_turn_duration = turn_duration
        self.heal_amount = heal_amount
    
    def on_apply(self):
        print(f"⛲️  {self.target.name} is regenerating health.")

    def on_expired(self):
        print(f"{self.target.name} is no longer regenerating health.")

    def on_new_turn(self):
        self.target.heal_damage(self.heal_amount // self.initial_turn_duration)


class StatusEffectBuff(Buff):
    def __init__(self, name, turn_duration, apply_chance, status_effect_flag, status_text, is_debuff=False):
        super().__init__(name, turn_duration, apply_chance, is_debuff=is_debuff)
        self.status_effect_flag = status_effect_flag
        self.status_text = status_text

    def on_new_turn(self):
        print(f"❕  {self.target.name} is {self.status_text}.")


class SpellEffectBuff(Buff):
    def __init__(self, name, turn_duration, spell_effects):
        super().__init__(name, turn_duration)
        self.spell_effects = spell_effects or []


# ===== FACTORY ======

def make_evasion():
    return BonusStatBuff("Evasion", 1, { BonusStat.DODGE: 10 })


def make_rage():
    return StatBuff("Rage", 3, { Stat.STRENGTH: 3, Stat.INTELLECT: -3 }, True)


def make_regen():
    return HOTBuff("Regen", 3, 1.0, 10)


def make_burn():
    return DOTBuff("Burn", 3, 0.7, 6, Elements.FIRE)


def make_paralysis():
    return StatusEffectBuff("Paralysis", 1, 0.2, BuffFlags.PREVENT_ACTION, "paralyzed", True)


def make_reflect():
    return StatusEffectBuff("Reflect", 2, 0.8, BuffFlags.REFLECT_MAGIC, "reflecting magic")



# ===== REGISTRY ======

buffs = {
    "burn": make_burn,
    "evasion": make_evasion,
    "rage": make_rage,
    "regen": make_regen,
    "paralysis": make_paralysis
}