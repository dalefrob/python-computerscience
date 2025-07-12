class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.inventory = []
    
    def move(self, x_dir : int, y_dir : int, map):
        self.x += x_dir
        self.y += y_dir
