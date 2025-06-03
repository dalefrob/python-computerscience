from enum import IntFlag
from pathlib import Path
import pygame as pg

path = Path(__file__).parent.resolve()

LIGHTCOLOR = (255, 220, 220)
DARKCOLOR = (200, 100, 100)

PIECE_TYPE_MASK =  0b00111
PIECE_COLOR_MASK = 0b11000

SCREENWIDTH = 800
SCREENHEIGHT = 600
SQUARESIZE = 64


class Piece(IntFlag):
    NoPiece = 0
    King = 1
    Pawn = 2
    Knight = 3
    Bishop = 4
    Rook = 5
    Queen = 6

    White = 8
    Black = 16


def load_piece_images(square_size = 32):
    result = {}
    img = pg.image.load(path / "assets/Pieces.png").convert_alpha()
    img_width = img.size[0]
    tile_size = img_width // 6

    p = [Piece.King, Piece.Queen, Piece.Bishop, Piece.Knight, Piece.Rook, Piece.Pawn]
    # Load white pieces
    for i in range(6):
        surf = img.subsurface((i * tile_size, 0), (tile_size, tile_size))
        key = p[i] | Piece.White
        result[key] = pg.transform.scale(surf, (square_size, square_size))
    # Load black pieces
    for i in range(6):
        surf = img.subsurface((i * tile_size, tile_size), (tile_size, tile_size))
        key = p[i] | Piece.Black
        result[key] = pg.transform.scale(surf, (square_size, square_size))
    return result



class Board():
    """
    Handles the logic of the game board.
    Does not worry about rendering.
    """
    def __init__(self):
        self.squares = [0] * 64

        # Add Some test pieces
        self.squares[19] = Piece.White | Piece.Bishop
        self.squares[33] = Piece.Black | Piece.Pawn
        self.squares[34] = Piece.White | Piece.Knight
        self.squares[51] = Piece.White | Piece.Rook
        self.squares[29] = Piece.Black | Piece.Queen
        self.squares[53] = Piece.Black | Piece.King

        self.selected_piece = 0
        self.selected_index = -1

        self.last_possible_moves = []


    def get_piece_name(self, piece : Piece):
        piece_color = piece & PIECE_COLOR_MASK
        piece_type = piece & PIECE_TYPE_MASK
        return f"{piece_color.name} {piece_type.name}"


    def query_square(self, square):
        piece = self.squares[square]
        if piece > 0:
            print(self.get_piece_name(piece))
        return piece


    def file_rank_to_square(self, file, rank):
        return (rank * 8) + file


    def get_file(self, square):
        return square % 8 # X
    

    def get_rank(self, square):
        return square // 8 # Y


    def get_file_rank(self, square : int):
        file = self.get_file(square)
        rank = self.get_rank(square)
        return (file, rank)


    def is_square_in_board(self, square) -> bool:
        return 0 <= square < 64 


    def try_move(self, from_square, to_square):
        piece_temp = self.squares[from_square]
        self.squares[to_square] = piece_temp
        self.squares[from_square] = Piece.NoPiece
        return True


    def can_capture(self, first, second):
        # Basic capture - Doesn't account for any other rules
        first_color = first & PIECE_COLOR_MASK
        second_color = second & PIECE_COLOR_MASK
        return first_color != second_color


    def get_possible_moves(self, piece, from_index):
        result = []
        piece_color = piece & PIECE_COLOR_MASK
        piece_type = piece & PIECE_TYPE_MASK
        vert_flip = -1 if piece_color == Piece.Black else 1
        match piece_type:
            case Piece.Pawn:
                result.append(from_index + (8 * vert_flip))
            case Piece.Bishop:
                result.extend(self.get_diagonal_moves(piece, from_index))
            case Piece.Rook:
                result.extend(self.get_straight_moves(piece, from_index))
            case Piece.Queen:
                result.extend(self.get_diagonal_moves(piece, from_index))
                result.extend(self.get_straight_moves(piece, from_index))
        print(from_index, result)
        self.last_possible_moves = result
        return result


    def get_diagonal_moves(self, piece, from_index):
        result = []
        # nw
        for i in range(1, 8):
            test_index = from_index + (i * -9)
            if self.is_square_in_board(test_index):
                # If theres a piece at location
                dest_piece = self.squares[test_index]
                if dest_piece > 0:
                    if not self.can_capture(piece, dest_piece):
                        break
                    result.append(test_index)
                    break
                    # empty square
                result.append(test_index)
                
            if self.get_file(test_index) == 0:
                break

        # ne
        for i in range(1, 8):
            test_index = from_index + (i * -7)
            if self.is_square_in_board(test_index):
                # If theres a piece at location
                dest_piece = self.squares[test_index]
                if dest_piece > 0:
                    if not self.can_capture(piece, dest_piece):
                        break
                    result.append(test_index)
                    break
                    # empty square
                result.append(test_index)
            if (test_index - 7) % 8 == 0:
                break
        # sw
        for i in range(1, 8):
            test_index = from_index + (i * 7)
            if self.is_square_in_board(test_index):
                # If theres a piece at location
                dest_piece = self.squares[test_index]
                if dest_piece > 0:
                    if not self.can_capture(piece, dest_piece):
                        break
                    result.append(test_index)
                    break
                    # empty square
                result.append(test_index)
            if test_index % 8 == 0:
                break
        # se
        for i in range(1, 8):
            test_index = from_index + (i * 9)
            if self.is_square_in_board(test_index):
                # If theres a piece at location
                dest_piece = self.squares[test_index]
                if dest_piece > 0:
                    if not self.can_capture(piece, dest_piece):
                        break
                    result.append(test_index)
                    break
                    # empty square
                result.append(test_index)
            if (test_index - 7) % 8 == 0:
                break

        return result


    def get_straight_moves(self, piece, from_index):
        result = []
        # left
        for i in range(1, 8):
            test_index = from_index - i
            if self.is_square_in_board(test_index):
                dest_piece = self.squares[test_index]
                if dest_piece > 0:
                    if not self.can_capture(piece, dest_piece):
                        break
                    result.append(test_index)
                    break
                # empty square
                result.append(test_index)
            if test_index % 8 == 0:
                break
        # right
        for i in range(1, 8):
            test_index = from_index + i
            if self.is_square_in_board(test_index):
                dest_piece = self.squares[test_index]
                if dest_piece > 0:
                    if not self.can_capture(piece, dest_piece):
                        break
                    result.append(test_index)
                    break
                # empty square
                result.append(test_index)
            if (test_index - 7) % 8 == 0:
                break
        # up
        for i in range(1, 8):
            test_index = from_index - (i * 8)
            if self.is_square_in_board(test_index):
                dest_piece = self.squares[test_index]
                if dest_piece > 0:
                    if not self.can_capture(piece, dest_piece):
                        break
                    result.append(test_index)
                    break
                # empty square
                result.append(test_index)

        # down
        for i in range(1, 8):
            test_index = from_index + (i * 8)
            if self.is_square_in_board(test_index):
                dest_piece = self.squares[test_index]
                if dest_piece > 0:
                    if not self.can_capture(piece, dest_piece):
                        break
                    result.append(test_index)
                    break
                # empty square
                result.append(test_index)

        return result




class BoardVisual():
    """
    Class designed to separate the rendering from the logic of the game board
    """
    def __init__(self, board : Board, square_size : int = 32):
        self.board = board
        self.square_size = square_size
        self.piece_images = load_piece_images(square_size)

        # Selection
        self.selected_square = None
        self.selected_piece = None
    

    def get_rect(self):
        half_size = self.square_size * 4
        center_screen = (SCREENWIDTH / 2, SCREENHEIGHT / 2)
        top_left = (center_screen[0] - half_size, center_screen[1] - half_size)
        return pg.Rect(top_left, (self.square_size * 8, self.square_size * 8))


    def handle_mouse_event(self, mouse_event):
        if mouse_event.type == pg.MOUSEBUTTONUP:
            # Left mouse button
            if mouse_event.button == 1:
                mouse_up_square = self.index_from_screen_pos(mouse_event.pos)
                # deselect selected square
                if self.selected_square == mouse_up_square:
                    self.deselect_square()
                # select
                elif self.selected_square == None:
                    self.select_square(mouse_up_square)
                # try move
                else:
                    self.try_move(mouse_up_square)
            if mouse_event.button == 3:
                # Right mouse button
                self.deselect_square()


    def deselect_square(self):
        print("Deselect")
        self.selected_square = None
        self.selected_piece = None
        self.board.last_possible_moves.clear()
        

    def select_square(self, square):
        piece = self.board.query_square(square)
        if piece > 0:
            self.selected_square = square
            print(f"Selected piece: {self.board.squares[square]} on square: {square}")
            self.selected_piece = piece
            self.board.get_possible_moves(piece, square)


    def try_move(self, to_square):
        print(f"Try move to {to_square}")
        if self.board.try_move(self.selected_square, to_square):
            self.deselect_square()


    def index_from_screen_pos(self, screen_pos):
        rect = self.get_rect()
        if rect.collidepoint(screen_pos):
            offset_x, offset_y = (screen_pos[0] - rect.topleft[0], screen_pos[1] - rect.topleft[1])
            col, row = offset_x // self.square_size, offset_y // self.square_size
            square = row * 8 + col
            return square


    def get_screen_position(self, col, row):
        rect = self.get_rect()
        x = rect.x + (col * self.square_size)
        y = rect.y + (row * self.square_size)
        return (x, y)


    def index_to_colrow(self, index):
        row = index % 8
        col = index // 8
        return col, row


    def get_square_rect(self, col, row):
        topleft = self.get_screen_position(col, row)
        return pg.Rect(topleft, (self.square_size, self.square_size))


    def render_board(self, dest_surface : pg.Surface):
        for index in range(len(self.board.squares)):
            col, row = self.index_to_colrow(index)
            rect = self.get_square_rect(row, col)

            surf = pg.Surface((self.square_size, self.square_size))
            is_light_square = (row + col) % 2 != 0
            square_color = LIGHTCOLOR if is_light_square else DARKCOLOR
            
            if index in board.last_possible_moves:
                square_color = pg.Color(square_color) % pg.Color(180, 230, 180)

            surf.fill(square_color)

            # board
            dest_surface.blit(surf, rect)

            # piece
            piece = self.board.squares[index]
            if piece > 0:
                piece_surf = self.piece_images[piece]
                dest_surface.blit(piece_surf, rect)

            # debugging
            text = font.render(f"{index}", True, (0, 0, 0))
            dest_surface.blit(text, rect)
            
            

# ------ START PROGRAM -------

pg.init()
screen = pg.display.set_mode((800,600))
pg.display.set_caption("Chess")
font = pg.font.SysFont(None, 18)
clock = pg.Clock()

board = Board()
board_visual = BoardVisual(board, 48)

def main():
    running = True
    while running:
        screen.fill((40,40,40))
        board_visual.render_board(screen)
        pg.display.flip()

        for event in pg.event.get():
            if event.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP]:
                board_visual.handle_mouse_event(event)
            if event.type == pg.QUIT:
                running = False
                pg.quit()
        clock.tick(15)


if __name__ == "__main__":
    main()