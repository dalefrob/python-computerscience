import random
from collections import deque
from helpers import *
from bloke import *
from spells import *
from items import *
from proc import *

class Battle():
    def __init__(self, initial_blokes):
        self.blokes = initial_blokes or []
        self.turn_queue = deque()
        self.new_defeated = []

        self.running = True
        self.winner = None

    def setup(self):
        bloke: Bloke
        for bloke in self.blokes:
            bloke.on_fatal_blow.connect(self.on_fatal_blow)
            self.turn_queue.append(bloke)
            print(bloke)
        

    def on_fatal_blow(self, bloke):
        self.trigger_proc(ProcTiming.ON_FATAL, ProcContext(bloke))
        self.new_defeated.append(bloke)


    def add_bloke(self, bloke):
        pass


    def mainloop(self):
        print(colored(MAGENTA, "The battle begins!\n"))
        while (not self.winner):
            # If turns remain, run them
            if len(self.turn_queue) > 1:
                bloke: Bloke = self.turn_queue.popleft()
                if not bloke.defeated:
                    self.do_turn(bloke)
            else:
                self.winner = self.turn_queue[0]
        
        print(colored(CYAN, f"🏆  Winner: {self.winner.name}"))


    def do_turn(self, bloke : Bloke):
        self.new_defeated.clear()
        turn_string = colored(LIGHTBLUE, f"\n{bloke.name}'s turn!")
        print(turn_string, f"HP:{bloke.hp}")

        # Trigger item procs at start of turn
        self.trigger_proc(ProcTiming.ON_TURNSTART, ProcContext(bloke))
        bloke.new_turn() 

        if bloke.can_act(): 
            if random.random() < 0.2:
                self.do_spell(bloke)
            else:
                self.do_melee(bloke)
        else:
            if not bloke.defeated:
                print(f"{bloke.name} is unable to move!")

        # do a defeated check
        for def_bloke in self.new_defeated:
            print(colored(GRAY, f"💀  {def_bloke.name} was defeated."))

        # If we're still alive, add oursleves back to the queue
        if not bloke.defeated:
            self.trigger_proc(ProcTiming.ON_TURNEND, ProcContext(bloke))
            self.turn_queue.append(bloke)


    def get_valid_targets(self, attacker: Bloke, num = 1):
        """ 
        Get a valid target from the list of blokes
        """
        targets = self.blokes.copy()
        targets = [t for t in self.blokes if t is not attacker and not t.defeated]

        if len(targets) <= num:
            num = len(targets)
        return random.sample(targets, k=num)  # Unique targets


    def do_spell(self, attacker: Bloke):
        spell: Spell = attacker.get_spell()
        defenders = self.get_valid_targets(attacker, num=spell.num_targets)
        spell.cast(attacker, defenders)


    def do_melee(self, attacker: Bloke):
        defender = self.get_valid_targets(attacker)[0]
        assert isinstance(defender, Bloke)
        if not defender:
            return
        
        print(f"{attacker.name} attacks {defender.name}!")

        # Test for dodge
        dodge_chance = defender.get_dodge_chance()
        roll = random.uniform(0, 100)
        if roll < dodge_chance:
            print(f"💨  {defender.name} dodged the attack.")
            return

        # Assume hit --
        dmg = attacker.get_damage()

        # Test for parry
        parry_chance = defender.get_parry_chance()
        roll = random.uniform(0, 100)
        if roll < parry_chance:
            self.trigger_proc(ProcTiming.ON_PARRY, ProcContext(defender, attacker))
            print(f"⚔️  {defender.name} parried!")
            attacker.take_damage(int(dmg / 2))
            return

        # Test for critical hit
        crit_happened = False
        crit_chance = attacker.get_crit_chance()
        roll = random.uniform(0, 100)
        if roll < crit_chance:
            print(colored((255, 0, 0),"♢ CRIT! ♢"))
            dmg *= 2
            self.trigger_proc(ProcTiming.ON_CRIT, ProcContext(attacker, defender))

            crit_happened = True

        if not crit_happened: # We don't want double procs - probably overpowered
            self.trigger_proc(ProcTiming.ON_HIT, ProcContext(attacker, defender))

        defender.take_damage(dmg)
        self.trigger_proc(ProcTiming.ON_TOOKDAMAGE, ProcContext(defender, attacker))

    
    def trigger_proc(self, proc_type, context = None):
        """
        Function runs at specific battle timimngs - Need to improve filtering
        """
        for proc in context.owner.item.get_procs(proc_type):
            assert isinstance(proc, Proc)
            if proc.should_trigger():
                proc.trigger(context)