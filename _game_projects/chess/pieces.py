import pygame as pg
from main import SQUARESIZE


# DO I NEED THESE CLASSES??

class Piece():
    def __init__(self, square, is_black):
        self.square = square
        self.is_black = is_black

    def get_possible_moves(self):
        return []



class Pawn(Piece):
    def __init__(self, is_black):
        super().__init__(is_black)
        self.has_moved = False

    def get_possible_moves(self):
        result = []
        if self.is_black:
            result.append(-8)
        else:
            result.append(8)


class Knight(Piece):
    def __init__(self, is_black):
        super().__init__(is_black)
    