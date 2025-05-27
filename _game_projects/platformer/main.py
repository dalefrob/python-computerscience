import pygame as pg
from pygame.locals import *
import sys

from src.enemy import Enemy
from src.player import Player
from src.tilemap import Level, TilemapLayer

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
        
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera.set_bounds(0, 0, 2000, 0)
        self.debug_font = pg.font.SysFont('Console', 8)

        self.player = None
        self.player_start = (0,0)
        self.entities = []

        # level
        self.level = Level(self, "Level_0")
        self.spawn_entities(self.level.entity_layers)
        for e in self.entities:
            e.ready()
    

    def spawn_player(self):
        if self.player:
            del self.player
        self.player = Player(self, self.player_start)


    def spawn_entities(self, entity_layers):
        for layer in entity_layers:
            for entity in layer:
                world_pos = entity["world_pos"]
                # Spawn appropriate entity
                match entity["name"]:
                    case "Player":
                        self.player_start = world_pos
                        self.spawn_player()
                    case "Mushroom":
                        enemy = Enemy(self, world_pos)
                        # Set properties in the calss if it has them
                        for key, value in entity["properties"].items():
                            if hasattr(enemy, key):
                                setattr(enemy, key, value)
                        self.entities.append(enemy)
        print("Spawned Entities")


    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # Convert milliseconds to seconds
            # update
            self.player.update(dt)
            # check out of bounds
            if self.player.pos.y > SCREEN_HEIGHT + 50:
                # auto destroy and spawn player
                self.spawn_player()

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
        self.level.render(self.screen, self.camera.offset)
        # Draw the player and apply the offset
        self.player.render(self.screen, self.camera.offset)
        # Draw the entities and apply the offset
        for entity in self.entities:
            entity.render(self.screen, self.camera.offset)


if __name__ == "__main__":
    game = Game()
    game.run()