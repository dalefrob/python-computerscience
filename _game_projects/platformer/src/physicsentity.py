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
        self.game = game

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

        # No collisions, just move
        if self.disable_collision == True:
            self.pos[0] += self.velocity[0] * dt * self.speed
            self.pos[1] += self.velocity[1] * dt * self.speed
            return

        # get nearest tiles
        map_coord = self.game.tilemap.world_to_map(self.rect().move(self.velocity[0] * dt * self.speed, self.velocity[0] * dt * self.speed).center)
        tile_rects = self.game.tilemap.get_neighbor_rects(map_coord)

        _new_pos = self.pos

        # Move vertically
        _test_rect = self.rect().move(0, self.velocity[1] * dt * self.speed)
        
        can_move = True
        # Check for vertical collisions
        for tile in collision_test(_test_rect, tile_rects):
            assert isinstance(tile, pg.Rect)
            if self.velocity[1] > 0:
                _new_pos[1] = tile.top - self.size[1]
                self.velocity[1] = 1 # IMPORTANT!!! --- Set this to 1 so that the character tries to collide with the ground next frame!
                self.on_floor = True
                can_move = False
            elif self.velocity[1] < 0:
                _new_pos[1] = tile.bottom
                self.on_ceiling = True
                can_move = False
        
        if can_move:
            _new_pos[1] += self.velocity[1] * dt * self.speed
        
        _test_rect = self.rect().move(self.velocity[0] * dt * self.speed, 0)
        can_move = True
        
        # Check for horizontal collisions
        for tile in collision_test(_test_rect, tile_rects):   # OLD --- self.game.tiles
            print("H Coll")
            if self.velocity[0] > 0:
                _new_pos[0] = tile.left - self.size[0]
            elif self.velocity[0] < 0:
                _new_pos[0] = tile.right
            self.on_wall = True
            can_move = False
            

        # Move horizontally
        if can_move:
            _new_pos[0] += self.velocity[0] * dt * self.speed

        self.pos = _new_pos
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