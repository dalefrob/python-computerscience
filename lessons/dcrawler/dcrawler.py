from room import Room
from player import Player

def print_map(map, player):
    # Print out all the rooms in the dungeon map
    for y in range(len(map)):
        rowstr = ""
        for x in range(len(map[y])):
            roomstr = "[ ]"
            if player.x == x and player.y == y:
                roomstr = "[P]"
            rowstr += f"({x},{y}) {roomstr}"
        print(rowstr)

def main():
    # Initialize the dungeon map with room objects
    dmap = [
        [Room("A dusty old classroom"), Room("A room with cracked walls"), None],
        [Room("The haunted bathroom"), Room("The bedroom"), Room("The slippery stairs")],
        [Room("The spooky backyard"), Room("The well"), Room("The foggy forest")]
    ]
    # Create the player object
    player = Player(0,0)
    print_map(dmap, player)
    player.move(1, 0, dmap) # Move the player --> in x
    print_map(dmap, player)

# Entry point into the program
if __name__ == "__main__":
    main()