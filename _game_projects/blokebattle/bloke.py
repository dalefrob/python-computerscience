from g_signal import Signal
from buff import *
from items import *
from spells import all_spells
from helpers import *
from weightedpicker import get_weighted_random
import random


class Bloke:
    def __init__(self, name):
        self.name = name
        self.buff_manager = BuffManager(self)
        # Stats
        self._base_stats = {
            stat: 3 for stat in Stat
        }
        self._base_bonus = {
            stat: 5 for stat in BonusStat
        }
        # Distribute 12 additional points randomly
        for _ in range(12):
            stat = random.choice(list(self._base_stats.keys()))
            self._base_stats[stat] += 1
        # Atts
        self.max_health = 10 + (self._base_stats[Stat.STAMINA] * 3)
        self.hp = self.max_health
        # items
        self.item = make_nullweapon()
        # Spells
        self.spells = [
            ("fireball", 10),
            ("shock", 10),
            ("cure", 8),
            ("curaga", 4)
        ]
        
        self.defeated = False
        self.on_fatal_blow = Signal()

    @property
    def strength(self):
        return self._get_stat_total(Stat.STRENGTH)

    @property
    def agility(self):
        return self._get_stat_total(Stat.AGILITY)
    
    @property
    def stamina(self):
        return self._get_stat_total(Stat.STAMINA)
    
    @property
    def intellect(self):
        return self._get_stat_total(Stat.INTELLECT)

    def _get_stat_total(self, stat_name : Stat):
        return self._base_stats[stat_name] + self.get_item_stats(stat_name) + self.get_stat_buffs(stat_name)

    def get_parry_chance(self):
        base_parry = self._base_bonus[BonusStat.PARRY]
        strength_factor = 0.2
        bonus = self.get_bonus_stat_buffs(BonusStat.PARRY)
        return base_parry + (self.strength * strength_factor) + bonus # + additional from buffs and items

    def get_crit_chance(self):
        base_crit = self._base_bonus[BonusStat.CRIT]
        agility_factor = 0.2
        bonus = self.get_bonus_stat_buffs(BonusStat.CRIT)
        return base_crit + (self.agility * agility_factor) + bonus # + additional from buffs and items

    def get_dodge_chance(self):
        base_dodge = self._base_bonus[BonusStat.DODGE]
        agility_factor = 0.4
        bonus = self.get_bonus_stat_buffs(BonusStat.DODGE)
        return base_dodge + (self.agility * agility_factor) + bonus # + additional from buffs and items
    
    def new_turn(self):
        self.buff_manager.new_turn()

    def get_damage(self):
        dmg = self.strength
        if isinstance(self.item, Weapon):
            dmg += self.item.get_damage()
        return round(dmg) 

    def get_spell(self):
        choice = get_weighted_random(self.spells)
        spell = all_spells[choice](self)
        return spell

    def take_damage(self, amount, element=None):
        self.hp -= amount

        element_string = "" if not element else element + " "
        damage_string = colored(RED, f"{amount} {element_string}damage!")
        print(f"{self.name} took {damage_string}")

        if self.hp <= 0 and not self.defeated:
            self.defeated = True
            self.on_fatal_blow.emit(self)

    def heal_damage(self, amount):
        self.hp += amount
        heal_string = colored(GREEN, str(amount))
        print(f"{self.name} healed for {heal_string}.")
        if self.hp > self.max_health:
            self.hp = self.max_health

    def get_status_effects(self):
        se_buffs = self.buff_manager.get_buffs_by_type(StatusEffectBuff)
        se_flags = 0
        for buff in se_buffs:
            assert isinstance(buff, StatusEffectBuff)
            se_flags |= buff.status_effect_flag
        return se_flags

    def get_item_stats(self, stat_name):
        return self.item.stat_dict.get(stat_name, 0)
        #return sum(buff.stat_dict.get(stat_name, 0) for buff in buffs)

    def get_stat_buffs(self, stat_name):
        buffs = self.buff_manager.get_buffs_by_type(StatBuff)
        return sum(buff.stat_dict.get(stat_name, 0) for buff in buffs)

    def get_bonus_stat_buffs(self, bonus_stat_name):
        buffs = self.buff_manager.get_buffs_by_type(BonusStatBuff)
        return sum(buff.bonus_stat_dict.get(bonus_stat_name, 0) for buff in buffs)

    def equip_item(self, item):
        self.item = item
        print(f"{self.name} equipped the {item.name}.")

    def can_act(self):
        buff_prevent_action = (self.get_status_effects() & BuffFlags.PREVENT_ACTION)
        result = not buff_prevent_action and not self.defeated
        return result


    def __str__(self):
        return f"{self.name}, Strength:{self.strength}, Agility:{self.agility}, Intellect:{self.intellect}, Stamina:{self.stamina}, HP:{self.hp}"
