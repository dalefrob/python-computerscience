import random
from collections import deque
from battle import *

print("Loading Bloke Battle...\n")

def gen_test_blokes():
    blokes = []

    boa = Bloke("Boa")
    boa.equip_item(make_weapon())
    blokes.append(boa)

    mimi = Bloke("Mimi")
    mimi.equip_item(make_healing_weapon())
    blokes.append(mimi)
    

    carter = Bloke("Ethan")
    carter.equip_item(make_fire_weapon())
    blokes.append(carter)

    dale = Bloke("David")
    dale.equip_item(make_ring())
    blokes.append(dale)

    cindy = Bloke("Cindy")
    cindy.buff_manager.add_buff(make_reflect())
    blokes.append(cindy)

    return blokes

battle = Battle(gen_test_blokes())

def main():
    print(colored(MAGENTA, "\n*** WELCOME TO BLOKE BATTLE! ***"))
    battle.setup()
    battle.mainloop()

if __name__ == "__main__":
    main()
