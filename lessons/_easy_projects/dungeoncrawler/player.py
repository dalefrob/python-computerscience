class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.inventory = []

    def move(self, direction, dungeon_map : list):
        map_width = len(dungeon_map[0])
        map_height = len(dungeon_map)
        dx, dy = 0, 0
        if direction == "north":
            dy = -1
        elif direction == "south":
            dy = 1
        elif direction == "west":
            dx = -1
        elif direction == "east":
            dx = 1
        else:
            return False, "Invalid direction."

        new_x = self.x + dx
        new_y = self.y + dy

        if 0 <= new_x < map_width and 0 <= new_y < map_height:
            if dungeon_map[new_y][new_x] == None:
                return False, "You hit a wall."
            self.x = new_x
            self.y = new_y
            return True, "You move " + direction + "."
        else:
            return False, "You hit a wall."
