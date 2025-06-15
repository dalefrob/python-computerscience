import random
from collections import deque
from battle import *

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

battle = Battle(gen_test_blokes())

def main():
    battle.setup()
    battle.mainloop()

if __name__ == "__main__":
    main()
