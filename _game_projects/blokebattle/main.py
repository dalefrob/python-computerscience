import random
from collections import deque
from bloke import *
from spells import Spell

blokes = []
turn_queue = deque()



def main():
  setup()
  main_loop()



def setup():
  """
  Called once before the simluation starts to set things up
  """
  blokes.append(Bloke("Ching"))
  blokes.append(Bloke("Ryan"))
  blokes.append(Bloke("Cindy"))

  bloke : Bloke
  for bloke in blokes:
    bloke.defeated.connect(on_bloke_defeated)
    bloke.took_damage.connect(on_bloke_took_damage)
    turn_queue.append(bloke)
  


def main_loop():
  """
  The main game loop until only one bloke remains
  """
  print("The battle begins!")
  gameover = False
  while(not gameover):
    # If turns remain, run them
    if len(turn_queue) > 1:
      bloke : Bloke = turn_queue.popleft()
      if bloke.can_act():
        do_turn(bloke)
    else:
      winning_bloke = turn_queue[0]
      print(f"Winner: {winning_bloke.name}")
      gameover = True



def do_turn(bloke : Bloke):
  print(f"{bloke.name}'s turn!")

  if random.random() < 0.2:
    do_spell(bloke)
  else:
    do_melee(bloke)

  # If we're still alive, add oursleves back to the queue
  if not bloke.is_dead():
    turn_queue.append(bloke)



def get_valid_targets(attacker : Bloke, num = 1):
  """ 
  Get a valid target from the list of blokes
  """
  targets = blokes.copy()
  targets = [t for t in blokes if t is not attacker and not t.is_dead()]

  if len(targets) <= num:
      num = len(targets)
  return random.sample(targets, k=num)  # Unique targets



def do_spell(attacker : Bloke):
  spell : Spell = attacker.get_spell()
  defenders = get_valid_targets(attacker, num=spell.num_targets)
  spell.cast(attacker, defenders)



def do_melee(attacker : Bloke):
  defender = get_valid_targets(attacker)[0]
  if not defender:
    return
  # Melee
  print(f"{attacker.name} attacks {defender.name}!")
  dmg = attacker.get_damage() + random.randrange(-2,2)

  # Test for parry
  if random.random() < 0.2:
      print(f"{defender.name} parried!")
      attacker.take_damage(int(dmg / 2))
      return

  # Test for critical hit
  if random.random() < 0.2:
    print("CRIT!")
    dmg *= 2
  
  defender.take_damage(dmg)



# Signal Callbacks

def on_bloke_took_damage(bloke, amount, element):
  element_string = "" if not element else element + " "
  print(f"{bloke.name} took {amount} {element_string}damage!")


def on_bloke_defeated(bloke):
  print(f"{bloke.name} was defeated.")



if __name__ == "__main__":
  main()