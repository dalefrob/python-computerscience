class Room:
    def __init__(self, description):
        self.description : str = description
        self.is_exit : bool = False

    def __str__(self):
        return "Room: " + self.description