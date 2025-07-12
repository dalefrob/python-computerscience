class Tile:
    def __init__(self, description, items=None, is_exit=False):
        self.description = description
        self.items = items or []
        self.is_exit = is_exit
