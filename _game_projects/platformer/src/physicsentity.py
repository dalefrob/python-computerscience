import pygame as pg
from src.tilemap import Tilemap

GRAVITY = 18.0

def collision_test(rect, list_rects):
    collisions = []
    for r in list_rects:
        if rect.colliderect(r):
            collisions.append(r)
    return collisions


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

        dx = self.velocity[0] * dt * self.speed
        dy = self.velocity[1] * dt * self.speed

        # No collisions, just move
        if self.disable_collision == True:
            self.pos += pg.Vector2(dx, dy)
            return

        # get nearest tiles
        map_coord = self.game.tilemap.world_to_map(self.rect().move(dx, dy).center)
        tile_rects = self.game.tilemap.get_neighbor_rects(map_coord) # Query all 9 rects - otherwise youd wuery the whole set of collision sets

        _test_rect = self.rect().move(dx, 0)

        # Check for horizontal collisions
        for tile_rect in collision_test(_test_rect, tile_rects):   # OLD --- self.game.tiles
            assert isinstance(tile_rect, pg.Rect)
            penetration = {
                "left": _test_rect.left - tile_rect.right,
                "right": _test_rect.right - tile_rect.left
            }
            if self.velocity[0] > 0:
                dx = 0
                #_new_pos[0] = tile_rect.left - self.size[0]
            elif self.velocity[0] < 0:
                dx = 0
                #_new_pos[0] = tile_rect.right
            self.on_wall = True
            

        # Move horizontally
        self.pos[0] += int(dx)

        # Move vertically
        _test_rect = self.rect().move(0, dy)
        
        # Check for vertical collisions
        for tile_rect in collision_test(_test_rect, tile_rects):
            assert isinstance(tile_rect, pg.Rect)
            penetration = {
                "floor": _test_rect.bottom - tile_rect.top,
                "ceiling": _test_rect.top - tile_rect.bottom
            }
            if self.velocity[1] > 0:
                dy = 0
                self.pos[1] = tile_rect.top - self.size[1] # Snap to floor
                self.velocity[1] = 1 # IMPORTANT!!! --- Set this to 1 so that the character tries to collide with the ground next frame!
                self.on_floor = True
            elif self.velocity[1] < 0:
                dy = 1
                #_new_pos[1] = tile.bottom
                self.on_ceiling = True
        
        self.pos[1] += int(dy) # Prevents any half steps up tiles
        
        self.last_collisions = self.rect().collideobjectsall(self.game.entities)


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