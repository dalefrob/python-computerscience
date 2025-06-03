import pygame as pg
from main import Piece, Board, PIECE_COLOR_MASK, PIECE_TYPE_MASK

class BoardPiece():
    """
    Visual representation of a piece on the board
    """
    def __init__(self, board : Board, piece : int, initial_square : int, rect_size : tuple):
        self.board = board
        self.piece_bit = piece
        self.square = initial_square

        self.piece_color = piece & PIECE_COLOR_MASK
        self.piece_type = piece & PIECE_TYPE_MASK

        self.rect = pg.Rect((0,0),rect_size)

    def is_white(self):
        return self.piece_color == Piece.White
    
    def is_king(self):
        return self.piece_type == Piece.King

    def is_pawn(self):
        return self.piece_type == Piece.Pawn
    
    def is_knight(self):
        return self.piece_type == Piece.Knight
    
    def is_bishop(self):
        return self.piece_type == Piece.Bishop
    
    def is_rook(self):
        return self.piece_type == Piece.Rook
    
    def is_queen(self):
        return self.piece_type == Piece.Queen

    def get_possible_moves(self):
        return []

    def get_pawn_moves(self):
        pass

