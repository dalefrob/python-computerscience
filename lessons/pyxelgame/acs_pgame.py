from __future__ import annotations
import pyxel
import math
import random

# Fix up the collision detection.
# Add your own feature to the game
# eg.   New Enemy
#       Player can be killed
#       Melee attack


TILESIZE = 8
solid_tiles = [(2,1), (3,1), (4,1), (5,0), (5,1), (6,0), (6,1)]


def get_tile(pos_x, pos_y):
    tm_x = math.floor(pos_x / TILESIZE)
    tm_y = math.floor(pos_y / TILESIZE)
    return pyxel.tilemaps[0].pget(tm_x, tm_y)


def is_colliding(a : Rect, b : Rect):
    return (
        a.x < b.x + b.w and    # Left of A is less than right of B
        a.x + a.w > b.x and    # Right of A is greater than left of B
        a.y < b.y + b.h and    # Top of A is less than bottom of B
        a.y + a.h > b.y        # Bottom of A is greater than top of B
    )


def normalize(x, y):
    magnitude = math.sqrt(x*x + y*y)
    if magnitude == 0: return x, y
    nx = x / magnitude
    ny = y / magnitude
    return nx, ny


class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    
    def get_area(self):
        return self.w * self.h

    def moved(self, dx, dy) -> Rect:
        return Rect(self.x + dx, self.y + dy, self.w, self.h)
    
    def __str__(self):
        return f"x:{int(self.x)} y:{int(self.y)} w:{self.w} h:{self.h}"


class Bullet:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.speed = 2.0
        self.life = 100
    
    def get_rect(self):
        return Rect(self.x, self.y, 1.4, 1.4)

    def update(self):
        nx, ny = normalize(self.dx, self.dy)
        self.x += nx * self.speed
        self.y += ny * self.speed
        self.life -= 1

    def draw(self, cam_x, cam_y):
        pyxel.circ(self.x - cam_x, self.y - cam_y, 2, 10)


class Player:
    def __init__(self, x, y, app : App):
        self.x = x
        self.y = y
        
        self.dx = 1
        self.dy = 0

        self.last_d = (0,0)
        self.room = (0,0)

        self.frame = 0
        self.time = 0

        self.app = app
    
    def get_center_pos(self):
        return self.x + 8, self.y + 12

    def get_rect(self) -> Rect:
        return Rect(self.x, self.y, 8, 16)

    def get_foot_rect(self) -> Rect:
        return Rect(self.x + 6, self.y + 10, 4, 6)

    def update(self):
        self.time += 1
        # reset dx and dy
        self.dx = 0
        self.dy = 0

        if (pyxel.btn(pyxel.KEY_RIGHT)):
            self.dx = 1
        elif (pyxel.btn(pyxel.KEY_LEFT)):
            self.dx = -1
            
        if (pyxel.btn(pyxel.KEY_UP)):
            self.dy = -1
        elif (pyxel.btn(pyxel.KEY_DOWN)):
            self.dy = 1
        
        # update the last direction if there was an input
        if self.dx != 0 or self.dy != 0:
            self.last_d = (self.dx, self.dy)

            if self.time % 8 == 0:
                self.frame += 1

        # can we move?
        coll = False
        current_rect = self.get_rect()
        future_rect = current_rect.moved(self.dx, self.dy)
        for rect in self.app.tile_rects:
            coll = is_colliding(rect, future_rect)
            if coll == True: break
        
        if not coll:
            self.x += self.dx
            self.y += self.dy
            
            cx, cy = self.get_center_pos()
            self.room = (cx // 128, cy // 128)
        
        # animate
        if self.frame > 1:
            self.frame = 0

        if(pyxel.btnp(pyxel.KEY_SPACE)):
            x, y = self.get_center_pos()
            tile = get_tile(x, y)
            print(tile)
            self.shoot()
    
    def shoot(self):
        new_bullet = Bullet(self.x + 8, self.y + 8, self.last_d[0], self.last_d[1])
        self.app.bullets.append(new_bullet)

    def draw(self):
        room_x, room_y = self.room
        screen_x = self.x - (room_x * 128)
        screen_y = self.y - (room_y * 128)

        pyxel.blt(screen_x, screen_y, 0, 0, 16 + (16 * self.frame), 16, 16, 8)


class Enemy:
    def __init__(self, x, y, app):
        self.x = x
        self.y = y
        self.speed = random.random() * 0.25
        self.app = app
    
    def get_rect(self) -> Rect:
        return Rect(self.x + 8, self.y, 8, 16)
    
    def get_foot_rect(self) -> Rect:
        return Rect(self.x + 6, self.y + 8, 4, 8)

    def update(self, player : Player):
        dx = player.x - self.x
        dy = player.y - self.y
        nx, ny = normalize(dx, dy)

        coll = False
        future_rect = self.get_foot_rect().moved(nx * self.speed, ny * self.speed)
        for tile in self.app.tile_rects:
            coll = is_colliding(tile, future_rect)
            if coll: break
        
        if not coll:
            self.x += nx * self.speed
            self.y += ny * self.speed

        
    def draw(self, cam_x, cam_y):
        pyxel.blt(self.x - cam_x, self.y - cam_y, 0, 16, 16, 16, 16, 8)


class App:
    def __init__(self):
        pyxel.init(128, 128, "My Game", 60)
        pyxel.load("my_resource.pyxres")

        self.bullets =  []

        self.tile_rects = []
        self.setup_tile_rects()

        self.player = Player(20, 60, self)
        self.enemies = [
            Enemy(100, 40, self),
            Enemy(110, 60, self),
            Enemy(110, 80, self)
        ]

        pyxel.run(self.update, self.draw)
    
    def setup_tile_rects(self):
        tilemap = pyxel.tilemaps[0]
        for i in range(tilemap.width):
            for j in range(tilemap.height):
                if tilemap.pget(i, j) in solid_tiles:
                    rect = Rect(i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE)
                    self.tile_rects.append(rect)
        

    def update(self):
        dt = 60/1000
        self.player.update()

        for b in self.bullets:
            assert isinstance(b, Bullet)
            b.update()
            for e in self.enemies:
                if is_colliding(b.get_rect(), e.get_rect()):
                    self.bullets.remove(b)
                    self.enemies.remove(e)
                    break
            if b.life < 0:
                self.bullets.remove(b)

        for e in self.enemies:
            e.update(self.player)

            player_rect = self.player.get_rect()
            enemy_rect = e.get_rect()

            if is_colliding(player_rect, enemy_rect):
                print("Colliding!")


    def draw_room(self):
        pyxel.bltm(0, 0, 0, self.player.room[0] * 128, self.player.room[1] * 128, 128, 128, 0)

    def get_camera_offset(self):
        rx, ry = self.player.room
        return rx * 128, ry * 128

    def draw(self):
        pyxel.cls(1)
        
        cam_x, cam_y = self.get_camera_offset()
        self.draw_room()

        for b in self.bullets:
            b.draw(cam_x, cam_y)

        self.player.draw()

        for e in self.enemies: 
            e.draw(cam_x, cam_y)
        
        for r in self.tile_rects:
            pyxel.rect(r.x, r.y, r.w, r.h, 14)

App()