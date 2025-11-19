class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
    
    def move(self, x_dir : int, y_dir : int, map) -> bool:
        new_x = self.x + x_dir
        new_y = self.y + y_dir

        if new_x < 0 or new_x >= len(map[0]):
            return False
        if new_y < 0 or new_y >= len(map):
            return False
        # [[-,p,-]
        #  [-,-,-]]   
        # When you move in y - you are changing row
        # Wen you move in x - you are changing column
        if map[new_y][new_x] == None:
            return False

        self.x = new_x
        self.y = new_y

        return True
