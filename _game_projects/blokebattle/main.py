import random
from collections import deque
from helpers import *
from bloke import *
from spells import *

blokes = []
turn_queue = deque()

def gen_test_blokes():
    blokes = []

    blokes.append(Bloke("Brad"))
    blokes.append(Bloke("Rob"))
    blokes.append(Bloke("Carter"))

    dale = Bloke("Dale")
    dale.equip_item(make_ring())
    blokes.append(dale)

    orion = Bloke("Orion")
    orion.spells.append(("doomsday", 15))
    orion.buff_manager.add_buff(make_reflect())
    blokes.append(orion)

    return blokes

#battle = Battle(gen_test_blokes())

def main():
    setup()
    main_loop()



def setup():
    """
    Called once before the simluation starts to set things up
    """
    #blokes.append(Bloke("Ching"))
    blokes.append(Bloke("Siren Head"))
    blokes.append(Bloke("Godzilla"))
    blokes.append(Bloke("Attack Titan"))
    sephi = Bloke("Sephiroth")
    sephi.equip_item(make_ring())
    blokes.append(sephi)
    #blokes.append(Bloke("Mimi"))
    #blokes.append(Bloke("Boa"))
    orion = Bloke("Orion the Destroyer")
    orion.spells.append(("doomsday", 15))
    orion.buff_manager.add_buff(make_reflect())
    blokes.append(orion)


    bloke: Bloke
    for bloke in blokes:
        bloke.on_defeated.connect(on_bloke_defeated)
        turn_queue.append(bloke)


def main_loop():
    """
    The main game loop until only one bloke remains
    """
    print(colored(MAGENTA, "\n*** WELCOME TO BLOKE BATTLE! ***"))
    for bloke in blokes:
        print(bloke)
    print("---------------------")
    print(colored(MAGENTA, "The battle begins!\n"))

    gameover = False
    while (not gameover):
        # If turns remain, run them
        if len(turn_queue) > 1:
            bloke: Bloke = turn_queue.popleft()
            if not bloke.defeated:
                do_turn(bloke)
        else:
            winning_bloke = turn_queue[0]
            print(colored(CYAN, f"🏆  Winner: {winning_bloke.name}"))
            gameover = True


new_defeated = []
def on_bloke_defeated(bloke):
    new_defeated.append(bloke)


def do_turn(bloke: Bloke):
    new_defeated.clear()
    turn_string = colored(LIGHTBLUE, f"\n{bloke.name}'s turn!")
    print(turn_string, f"HP:{bloke.hp}")

    bloke.new_turn() 

    if bloke.can_act(): 
        if random.random() < 0.2:
            do_spell(bloke)
        else:
            do_melee(bloke)
    else:
        if not bloke.defeated:
            print(f"{bloke.name} is unable to move!")

    # do a defeated check
    for def_bloke in new_defeated:
        print(colored(GRAY, f"💀  {def_bloke.name} was defeated."))

    # If we're still alive, add oursleves back to the queue
    if not bloke.defeated:
        turn_queue.append(bloke)


def get_valid_targets(attacker: Bloke, num = 1):
    """ 
    Get a valid target from the list of blokes
    """
    targets = blokes.copy()
    targets = [t for t in blokes if t is not attacker and not t.defeated]

    if len(targets) <= num:
        num = len(targets)
    return random.sample(targets, k=num)  # Unique targets


def do_spell(attacker: Bloke):
    spell: Spell = attacker.get_spell()
    defenders = get_valid_targets(attacker, num=spell.num_targets)
    spell.cast(attacker, defenders)


def do_melee(attacker: Bloke):
    defender = get_valid_targets(attacker)[0]
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

    # Trigger ON_HIT procs
    for proc in attacker.item.get_procs(ProcTiming.ON_HIT):
        if proc.should_trigger():
            result = proc.trigger(attacker, defender, context={ })
            if result:
                extra_damage = round(result.get("extra_damage", 0))
                dmg += extra_damage

    # Test for parry
    parry_chance = defender.get_parry_chance()
    roll = random.uniform(0, 100)
    if roll < parry_chance:
        print(f"⚔️  {defender.name} parried!")
        attacker.take_damage(int(dmg / 2))
        return

    # Test for critical hit
    crit_chance = attacker.get_crit_chance()
    roll = random.uniform(0, 100)
    if roll < crit_chance:
        print(colored((255, 0, 0),"♢ CRIT! ♢"))
        dmg *= 2

    defender.take_damage(dmg)




if __name__ == "__main__":
    main()
