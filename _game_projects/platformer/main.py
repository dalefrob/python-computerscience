import pygame as pg
from pygame.locals import *
import sys

from src.enemy import Enemy
from src.player import Player
from src.tilemap import Tilemap

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
FPS = 60
SKYBLUE = (50, 100, 200)


class Camera:
    def __init__(self, width, height):
        self.offset = pg.Vector2(0, 0)
        self.width = width
        self.height = height
        self.camera_bounds = [0, 0, 10000, 10000]

    def set_bounds(self, left, top, right, bottom):
        self.camera_bounds[0] = left
        self.camera_bounds[1] = top
        self.camera_bounds[2] = right
        self.camera_bounds[3] = bottom

    def update(self, target):
        # Center the camera on the target
        self.offset.x = pg.math.clamp(target.rect().centerx - self.width // 2, self.camera_bounds[0], self.camera_bounds[2])
        self.offset.y = pg.math.clamp(target.rect().centery - self.height // 2, 0, self.camera_bounds[3] - self.camera_bounds[1])


class Game():
    def __init__(self):
        pg.init()
        pg.font.init() # you have to call this at the start
        flags = pg.SCALED
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.player = Player(self, (96, 96), (24, 28))
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera.set_bounds(0, 0, 2000, 0)
        self.debug_font = pg.font.SysFont('Console', 8)

        # objects
        self.tilemap = Tilemap(self, 64, 16, 16)
        # self.tiles = [pg.Rect(600,150,50,50), pg.Rect(400,150,50,50), pg.Rect(50,200,500,50), pg.Rect(200,150,50,50)]
        self.entities = []
        #enemy = Enemy(self, (300, 96), (26, 26))
        #self.entities.append(enemy)
    
    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # Convert milliseconds to seconds
            # update
            self.player.update(dt)
            for entity in self.entities:
                entity.update(dt)

            self.camera.update(self.player)

            # draw
            self.render_world()

            # events
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()
                # player
                self.player.handle_event(event)

            pg.display.flip()
    

    def render_world(self):
        self.screen.fill(SKYBLUE)

        # Camera offset
        offset_x, offset_y = self.camera.offset
        
        # Only draw tiles in view
        # for tile in self.tiles:
        #     if tile.colliderect(pg.Rect(offset_x, offset_y, SCREEN_WIDTH, SCREEN_HEIGHT)):
        #         # Apply camera offset
        #         adjusted_tile = tile.move(-offset_x, -offset_y)
        #         pg.draw.rect(self.screen, (255, 255, 0), adjusted_tile)
        
        self.tilemap.render(self.screen, self.camera.offset)
        # Draw the player and apply the offset
        self.player.render(self.screen, self.camera.offset)
        for entity in self.entities:
            entity.render(self.screen, self.camera.offset)


if __name__ == "__main__":
    game = Game()
    game.run()