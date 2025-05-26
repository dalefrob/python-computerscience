import pygame as pg
import math
from src.tilemap import TilemapLayer, Tile

GRAVITY = 18.0

def collision_test(rect, list_rects):
    collisions = []
    for r in list_rects:
        if rect.colliderect(r):
            collisions.append(r)
    return collisions


def collision_test_tile(rect, tile_list):
    collision_tiles = []
    for t in tile_list:
        assert isinstance(t, Tile)
        if rect.colliderect(t.get_rect()):
            collision_tiles.append(t)
    return collision_tiles


class PhysicsEntity():
    def __init__(self, game, pos, size):
        from main import Game
        self.game : Game = game

        # spatial vars
        self.pos = pg.Vector2(pos)
        self.size = size
        self.direction = 1
        self.velocity = pg.Vector2(0,0)
        self.speed = 50.0

        # collisions
        self.disable_collision = False
        self.on_floor = False
        self.on_ceiling = False
        self.on_wall = False
        self.last_collisions = []


    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])


    def update(self, dt):
        pass


    def move_and_collide(self, dt):
        # reset collision test
        self.on_wall = False
        self.on_floor = False
        self.on_ceiling = False

        dx = self.velocity[0] * dt
        dy = self.velocity[1] * dt

        # No collisions, just move
        if self.disable_collision == True:
            self.pos += pg.Vector2(dx, dy)
            return

        # get nearest tiles
        fglayer : TilemapLayer = self.game.level.get_fg_layer()
        map_coord = fglayer.world_to_map(self.rect().move(dx, dy).center)
        tile_rects = fglayer.get_neighbor_rects(map_coord) # Query all 9 rects - otherwise youd query the whole set of collision sets
        tiles = fglayer.get_neighbor_tiles(map_coord)

        _test_rect = self.rect().move(math.ceil(dx*2), 0)

        # Check for horizontal collisions
        for tile in collision_test_tile(_test_rect, tiles):   # OLD --- self.game.tiles
            assert isinstance(tile, Tile)
            tile_rect = tile.get_rect()
            penetration = {
                "left": _test_rect.left - tile_rect.right,
                "right": _test_rect.right - tile_rect.left
            }
            if self.velocity[0] > 0:
                dx = 0
            elif self.velocity[0] < 0:
                dx = 0
            self.on_wall = True
            

        # Move horizontally
        self.pos[0] += dx

        # Move vertically
        _test_rect = self.rect().move(0, math.ceil(dy)) # Gotta round this to make sure pixel snapping happens

        # Check for vertical collisions
        for tile in collision_test_tile(_test_rect, tiles):
            assert isinstance(tile, Tile)
            tile_rect = tile.get_rect()
            penetration = {
                "floor": _test_rect.bottom - tile_rect.top,
                "ceiling": _test_rect.top - tile_rect.bottom
            }
            if self.velocity[1] > 0:
                dy = 0
                self.pos[1] = tile_rect.top - self.size[1] # Snap to floor
                self.velocity[1] = 1 # IMPORTANT!!! --- Set this to 1 so that the character tries to collide with the ground next frame!
                self.on_floor = True
            elif self.velocity[1] < 0 and tile.collision == Tile.TILE_SOLID:
                dy = 1
                self.on_ceiling = True
        
        if not self.on_floor:
            self.pos[1] += dy
        
        self.last_collisions = self.rect().collideobjectsall(self.game.entities)


    def render_debug(self, surface, offset):
        text_surface = self.game.debug_font.render(f"v:{self.velocity}", False, (0, 0, 0))
        surface.blit(text_surface, self.rect().move(-offset.x, -offset.y - 8))


    def render(self, surface, offset):
        pg.draw.rect(surface, (255, 0, 0), self.rect().move(-offset.x, -offset.y))


def load_animation_frames(imgpath, columns, rows):
    frames = []
    img = pg.image.load(imgpath).convert_alpha()
    frame_width = img.width // columns
    frame_height = img.height // rows
    for f_y in range(rows):
        for f_x in range(columns):
            surf = img.subsurface(pg.Rect(frame_width * f_x, frame_height * f_y, frame_width, frame_height))
            frames.append(surf)
    return frames