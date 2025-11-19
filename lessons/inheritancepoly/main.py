from enemies import *

enemy = Enemy("Rat", 20, 15)
enemy2 = Dragon("Zyzix", 50, 20, "Ice")

def do_attack(attacker : Enemy, defender : Enemy):
    defender.take_damage(attacker.attack_power)

gameover = False
while not gameover:
    do_attack(enemy, enemy2)
    if enemy2.hp < 0:
        print(enemy.name, "wins")
        break
    do_attack(enemy2, enemy)
    if enemy.hp < 0:
        print(enemy2.name, "wins")
        break






# enemies = [enemy, enemy2]
# for e in enemies:
#     # Checks to see if 'e' is an Enemy object (instance)
#     assert isinstance(e, Enemy) 
#     e.attack()