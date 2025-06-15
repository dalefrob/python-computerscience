import random
from collections import deque
from battle import *

print("Loading Bloke Battle...\n")

def gen_test_blokes():
    blokes = []

    brad = Bloke("Brad")
    brad.equip_item(make_weapon())
    blokes.append(brad)
    
    blokes.append(Bloke("Rob"))

    carter = Bloke("Carter")
    carter.equip_item(make_fire_weapon())
    blokes.append(carter)

    dale = Bloke("Dale")
    dale.equip_item(make_ring())
    blokes.append(dale)

    orion = Bloke("Orion")
    orion.spells.append(("doomsday", 15))
    orion.buff_manager.add_buff(make_reflect())
    blokes.append(orion)

    return blokes

battle = Battle(gen_test_blokes())

def main():
    print(colored(MAGENTA, "\n*** WELCOME TO BLOKE BATTLE! ***"))
    battle.setup()
    battle.mainloop()

if __name__ == "__main__":
    main()
