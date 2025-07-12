import random
from player import Player
from tile import Tile

# color
def colored(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

class Game:
    def __init__(self):
        self.map = self.create_map()
        self.map[2][random.randint(0, 2)].is_exit = True
        self.player = Player()
        self.player.x = random.randint(0,2)
        self.running = True

    def create_map(self):
        return [
            [Tile("A dark room.", ["torch"]), Tile("A dusty hall."), Tile("An empty chamber.")],
            [Tile("A narrow corridor."), Tile("A room with a chest.", ["key"]), None],
            [Tile("A mossy cellar."), Tile("A glowing room."), Tile("A leaky ceiling.")],
        ]

    def print_map(self):
        print("Dungeon Map:\n")
        for y, row in enumerate(self.map):
            row_display = ""
            for x, tile in enumerate(row):
                if self.player.x == x and self.player.y == y:
                    row_display += "[P]"
                elif tile == None:
                    row_display += "  "
                else:
                    row_display += "[ ]"
            print(row_display)

    def current_tile(self):
        return self.map[self.player.y][self.player.x]

    def describe_current_tile(self):
        tile = self.current_tile()
        print(colored(255, 255, 0, f"{tile.description}"))

    def look(self):
        tile = self.current_tile()
        if tile.items:
            print("You see:", ", ".join(tile.items))
        else:
            print("There's nothing here.")

    def handle_input(self, command):
        command = command.lower()

        if command in ["north", "south", "east", "west"]:
            moved, msg = self.player.move(command, self.map)
            if moved:
                self.describe_current_tile()
                print(colored(80, 255, 255, msg))
            else:
                print(colored(255, 20, 20, msg))
        
        elif command == "take":
            tile = self.current_tile()
            if tile.items:
                item = tile.items.pop()
                self.player.inventory.append(item)
                print(f"You took the {item}.")
            else:
                print("There's nothing to take.")
        
        elif command == "inventory":
            print("You have:", ", ".join(self.player.inventory) or "nothing.")
        
        elif command == "look":
            self.look()
        
        elif command == "map":
            self.print_map()
        
        elif command == "quit":
            self.running = False
        
        else:
            print("Commands: north, south, east, west, take, map, inventory, look, quit")

    def check_victory(self):
        if self.current_tile().is_exit:
            print("\n🎉 You found the exit! You win!")
            self.running = False

    def start(self):
        print("Welcome to the Dungeon Crawler!")
        print("Commands: north, south, east, west, take, inventory, look, quit")
        self.print_map()
        self.describe_current_tile()
        while self.running:
            command = input("> ").strip()
            self.handle_input(command)
            self.check_victory()

        print("Game over.")
