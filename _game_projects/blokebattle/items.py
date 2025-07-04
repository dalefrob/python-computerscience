import random
from helpers import *
from proc import *
from spells import *
from buff import *


class Equipment():
    def __init__(self, name = "*equipment*", stat_dict = None, procs=None):
        self.name = name
        self.stat_dict = stat_dict or {}
        self.procs = procs or []
        for proc in self.procs:
            proc.set_source(self)

    
    def get_procs(self, timing):
        return [proc for proc in self.procs if timing in proc.proc_timing]


class Weapon(Equipment):
    def __init__(self, name, stat_dict, procs, dmg_min, dmg_max):
        super().__init__(name, stat_dict, procs)
        self.dmg_min = dmg_min
        self.dmg_max = dmg_max
    
    def get_damage(self):
        return random.randint(self.dmg_min, self.dmg_max)






# ===== ITEM FACTORY =====

def make_nullweapon():
    return Weapon("Null", {}, None, 0, 0)

def make_weapon():
    weapon = Weapon("Aqua Sword", { Stat.STRENGTH: 2, Stat.INTELLECT: 1 }, [AddMultDamage(ProcTiming.ON_HIT | ProcTiming.ON_CRIT, 0.25, 1.5, Elements.WATER)], 2, 4)
    return weapon

def make_fire_weapon():
    fire_effect = DealDamage(base_damage=2, element=Elements.FIRE)
    proc = EffectProc(ProcTiming.ON_HIT, 0.5, fire_effect)
    return Weapon("Fire Sword", {}, [proc], 2, 4)

def make_ring():
    ring = Equipment("Ring of Evasion", { Stat.AGILITY: 5 }, [CastBuffProc(ProcTiming.ON_TOOKDAMAGE, 0.5, make_evasion(), True)])
    return ring

def make_healing_weapon():
    weapon = Weapon(
        "Vampire Sword",
        { Stat.STRENGTH: 2 },
        [HealOnHitProc(ProcTiming.ON_HIT, 0.5, 2)],
        2, 4
    )
    return weapon