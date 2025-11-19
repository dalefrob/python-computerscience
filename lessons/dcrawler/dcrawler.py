from room import Room
from player import Player
import random

# color
def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"
#colored(0, 255, 0,"[P]")  # This will return a green "[P]"

def print_map(map, player):
    # Print out all the rooms in the dungeon map
    for row in range(len(map)):
        rowstr = ""
        for col in range(len(map[row])):
            roomstr = "[ ]"
            if map[row][col] == None:
                roomstr = "   "
            if player.x == col and player.y == row:
                roomstr = colored(0,255,0,"[P]")
            rowstr += f"{roomstr}"
        print(rowstr)

def add_treasure(map):
    for row in range(len(map)):
        for col in range(len(map[row])):
           rng = random.random()
           if rng < 0.5:
               room : Room = map[col][row]
               if room:
                gold = random.randint(1,99)
                room.treasure.append(f"{gold} Gold")

def main():
    # Initialize the dungeon map with room objects
    dmap = [
        [Room("A dusty old classroom"), Room("A room with cracked walls"), None],
        [None, Room("The bedroom"), Room("The slippery stairs")],
        [Room("The spooky backyard"), Room("The well"), Room("The foggy forest")]
    ]
    randx = random.randrange(0,2)
    dmap[2][randx].is_exit = True
    add_treasure(dmap)
    # Create the player object
    player = Player(0,0)
    print_map(dmap, player)
    # TODO - Make a basic game loop.
    gameover = False
    while not gameover:
        command = input("Enter command (exit, N, E, S, W): ")
        did_move = False
        match command:
            case "exit":
                gameover = True
                break
            case "S":
                did_move = player.move(0, 1, dmap)
                print_map(dmap, player)
            case "E":
                did_move = player.move(1, 0, dmap)
                print_map(dmap, player)
            case "N":
                did_move = player.move(0, -1, dmap)
                print_map(dmap, player)
            case "W":
                did_move = player.move(-1, 0, dmap)
                print_map(dmap, player)

        if did_move == True:
            print("Player Moved")
            current_room : Room = dmap[player.y][player.x]
            # Add treasure
            if len(current_room.treasure) > 0:
                for t in current_room.treasure:
                    player.inventory.append(t)

            print(colored(255,255,0,current_room.description))
            if current_room.is_exit:
                gameover = True
                print("🌟 Congratulations!🌟 You got to the exit!")
                print(colored(255,180,0, f"Your treasure: {player.inventory}"))
                break
        else:
            print("Could not move!")

    # While not gameover:
    #   Show possible commands - north, east, south, west, look, take, map
    #   Get player input, and validate it
    #   Act on input
    #   If player is in exit room:
    #       Break loop wth YOU WIN
    #   If player dies in a trap:
    #       Break loop with GAME OVER

# Entry point into the program
if __name__ == "__main__":
    main()