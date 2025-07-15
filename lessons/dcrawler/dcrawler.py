from room import Room
from player import Player

def print_map(map, player):
    # Print out all the rooms in the dungeon map
    for y in range(len(map)):
        rowstr = ""
        for x in range(len(map[y])):
            roomstr = "[ ]"
            if map[x][y] == None:
                roomstr = "   "
            if player.x == x and player.y == y:
                roomstr = "[P]"
            rowstr += f"{roomstr}"
        print(rowstr)

def main():
    # Initialize the dungeon map with room objects
    dmap = [
        [Room("A dusty old classroom"), Room("A room with cracked walls"), None],
        [None, Room("The bedroom"), Room("The slippery stairs")],
        [Room("The spooky backyard"), Room("The well"), Room("The foggy forest")]
    ]
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
            current_room : Room = dmap[player.x][player.y]
            print(current_room.description)
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