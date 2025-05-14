import pygame as pg
from pygame.locals import *
import sys
import os

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
FPS = 60

SKYBLUE = (50, 100, 200)

pg.font.init() # you have to call this at the start, 
                   # if you want to use this module.
my_font = pg.font.SysFont('Comic Sans MS', 12)


# resources
path = os.path.dirname(__file__)
path_idle = path + "/assets/Main Characters/Ninja Frog/Idle (32x32).png"
path_run = path + "/assets/Main Characters/Ninja Frog/Run (32x32).png"
path_jump = path + "/assets/Main Characters/Ninja Frog/Jump (32x32).png"
path_fall = path + "/assets/Main Characters/Ninja Frog/Fall (32x32).png"

tiles = [pg.Rect(600,150,50,50), pg.Rect(400,150,50,50), pg.Rect(50,200,500,50), pg.Rect(200,150,50,50)]


class PhysicsEntity():
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = pg.Vector2(pos)
        self.size = size
        self.velocity = pg.Vector2(0,0)
        self.speed = 50.0
        self.on_floor = False
        self.on_wall = False

    def rect(self):
        return pg.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, dt):
        self.velocity[1] += 18.0 * dt # Add gravity
        self.move(dt) # try to move

    def move(self, dt):
        # reset collision test
        self.on_wall = False

        # Update position based on velocity, delta time, and speed
        self.pos[0] += self.velocity[0] * dt * self.speed

        # Check for horizontal collisions
        for tile in collision_test(self.rect(), tiles):
            if self.velocity[0] > 0:
                self.pos[0] = tile.left - self.size[0]
            elif self.velocity[0] < 0:
                self.pos[0] = tile.right
            self.on_wall = True

        # Update vertical position
        self.pos[1] += self.velocity[1] * dt * self.speed
        # Check for vertical collisions
        for tile in collision_test(self.rect(), tiles):
            if self.velocity[1] > 0:
                self.pos[1] = tile.top - self.size[1]
                self.velocity[1] = 0
                self.on_floor = True
            elif self.velocity[1] < 0:
                self.pos[1] = tile.bottom


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


class Enemy(PhysicsEntity):
    IDLE = 0
    RUN = 1
    HIT = 2

    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.render_offset = [-3,0]
        # states
        self.current_state = self.IDLE

        # animation setup
        idle = path + "/assets/Enemies/Mushroom/Idle (32x32).png"
        run = path + "/assets/Enemies/Mushroom/Run (32x32).png"
        hit = path + "/assets/Enemies/Mushroom/Hit.png"
        self.animations = {
            "idle": load_animation_frames(idle, 14, 1),
            "run": load_animation_frames(run, 16, 1),
            "hit": load_animation_frames(hit, 5, 1)
        }
        self.current_animation = "run"
        self.last_update = 0
        self.frame_index = 0
        self.direction = -1
    
    def update(self, dt):
        super().update(dt)
        # animate frames
        now = pg.time.get_ticks()
        if now - self.last_update > 60:  # 700 ms
            self.animate(dt)
            self.last_update = now  # Reset the timer
    
    def animate(self, dt):
        self.frame_index += 1
        if self.frame_index > len(self.animations[self.current_animation]) - 1:
            self.frame_index = 0

    def move(self, dt):
        self.velocity[0] = self.direction * 0.5
        super().move(dt)
        if self.on_wall:
            self.direction *= -1

    def render(self, surface, offset):
        adjusted_rect = self.rect().move(-offset.x, -offset.y)
        #pg.draw.rect(surface, (0, 255, 0), adjusted_rect, 1)
        if self.direction == 1:
            surface.blit(pg.transform.flip(self.animations[self.current_animation][self.frame_index], True, False), adjusted_rect.move(self.render_offset[0], self.render_offset[1]))
        else:
            surface.blit(self.animations[self.current_animation][self.frame_index], adjusted_rect.move(self.render_offset[0], self.render_offset[1]))


class Player(PhysicsEntity):
    """
    The player 
    Contains animations
    """
    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.render_offset = [-4,0]
        self.inputs = {
            "right": False,
            "left": False,
            "up": False,
            "down": False
        }
        # animation
        self.direction = 1
        self.animations = {
            "idle": load_animation_frames(path_idle, 11, 1),
            "run": load_animation_frames(path_run, 12, 1),
            "jump": load_animation_frames(path_jump, 1, 1),
            "fall": load_animation_frames(path_fall, 1, 1)
        }
        self.current_animation = "idle"
        self.last_update = 0
        self.frame_index = 0
    
    
    def update(self, dt):
        super().update(dt)
        # horizontal logic
        if self.inputs["right"]:
            self.direction = 1
            self.velocity[0] = 3
            if self.on_floor:
                self.change_animation("run")
        elif self.inputs["left"]:
            self.direction = -1
            self.velocity[0] = -3
            if self.on_floor:
                self.change_animation("run")
        elif self.inputs["left"] + self.inputs["right"] == 0:
            self.velocity[0] = 0

        # vertical logic
        if not self.on_floor:
            if self.velocity[1] > 0:
                self.change_animation("fall")
            else:
                self.change_animation("jump")
        else:
            if self.velocity[0] == 0:
                self.change_animation("idle")

        # animate frames
        now = pg.time.get_ticks()
        if now - self.last_update > 60:  # 700 ms
            self.animate(dt)
            self.last_update = now  # Reset the timer


    def change_animation(self, next_animation_name):
        if self.current_animation != next_animation_name:
            self.frame_index = 0
            self.current_animation = next_animation_name

    def jump(self):
        self.velocity[1] = -7
        self.on_floor = False

    def animate(self, dt):
        self.frame_index += 1
        if self.frame_index > len(self.animations[self.current_animation]) - 1:
            self.frame_index = 0

    def render(self, surface, offset):
        adjusted_rect = self.rect().move(-offset.x + self.render_offset[0], -offset.y + self.render_offset[1])
        if self.direction == -1:
            surface.blit(pg.transform.flip(self.animations[self.current_animation][self.frame_index], True, False), adjusted_rect)
        else:
            surface.blit(self.animations[self.current_animation][self.frame_index], adjusted_rect)
        
        text_surface = my_font.render(f"vel: {self.velocity}", False, (0, 0, 0))
        surface.blit(text_surface, (0,0))
    

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                self.inputs["right"] = True
            if event.key == K_LEFT:
                self.inputs["left"] = True
            if event.key == K_UP:
                self.inputs["up"] = True
            if event.key == K_DOWN:
                self.inputs["down"] = True
            if event.key == K_SPACE and self.on_floor:
                self.jump()
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                self.inputs["right"] = False
            if event.key == K_LEFT:
                self.inputs["left"] = False
            if event.key == K_UP:
                self.inputs["up"] = False
            if event.key == K_DOWN:
                self.inputs["down"] = False


def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions


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
        flags = pg.SCALED
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.running = True
        self.player = Player(self, (50, 10), (24, 32))
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera.set_bounds(0, 0, 2000, 0)
        self.entities = []
        enemy = Enemy(self, (300, 10), (26, 32))
        # self.entities.append(enemy)
    
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
        for tile in tiles:
            if tile.colliderect(pg.Rect(offset_x, offset_y, SCREEN_WIDTH, SCREEN_HEIGHT)):
                # Apply camera offset
                adjusted_tile = tile.move(-offset_x, -offset_y)
                pg.draw.rect(self.screen, (255, 255, 0), adjusted_tile)
        
        # Draw the player and apply the offset
        self.player.render(self.screen, self.camera.offset)
        for entity in self.entities:
            entity.render(self.screen, self.camera.offset)


if __name__ == "__main__":
    game = Game()
    game.run()