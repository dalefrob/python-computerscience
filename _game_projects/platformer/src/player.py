import pygame as pg
from pathlib import Path
from src.enemy import *

# resources
path = Path(__file__).parent.resolve()

class Player(PhysicsEntity):
    """
    The player 
    Contains animations
    """
    def __init__(self, game, pos):
        super().__init__(game, pos, (16, 28))
        self.render_offset = [-8,-4]
        self.inputs = {
            "right": False,
            "left": False,
            "up": False,
            "down": False
        }

        path_idle = path / "../assets/Main Characters/Ninja Frog/Idle (32x32).png"
        path_run = path / "../assets/Main Characters/Ninja Frog/Run (32x32).png"
        path_jump = path / "../assets/Main Characters/Ninja Frog/Jump (32x32).png"
        path_fall = path / "../assets/Main Characters/Ninja Frog/Fall (32x32).png"

        self.animations = {
            "idle": load_animation_frames(path_idle, 11, 1),
            "run": load_animation_frames(path_run, 12, 1),
            "jump": load_animation_frames(path_jump, 1, 1),
            "fall": load_animation_frames(path_fall, 1, 1)
        }
        self.current_animation = "idle"
        self.last_update = 0
        self.frame_index = 0
        # att
        self.speed = 120.0
        self.jump_strength = 350


    def update(self, dt):
        self.velocity[1] += GRAVITY # Add gravity

        # horizontal logic
        if self.inputs["right"]:
            self.direction = 1
            self.velocity[0] = self.speed
            if self.on_floor:
                self.change_animation("run")
        elif self.inputs["left"]:
            self.direction = -1
            self.velocity[0] = -self.speed
            if self.on_floor:
                self.change_animation("run")
        elif self.inputs["left"] + self.inputs["right"] == 0:
            self.velocity[0] = 0

        self.move_and_collide(dt)

        # vertical logic
        if not self.on_floor:
            if self.velocity[1] > 0:
                self.change_animation("fall")
            else:
                self.change_animation("jump")
                if self.on_ceiling:
                    self.velocity[1] = 0
        else:
            if self.velocity[0] == 0:
                self.change_animation("idle")

        # entity collisions
        if self.last_collisions:
            for coll in self.last_collisions:
                if isinstance(coll, Enemy):
                    assert isinstance(coll, Enemy)
                    if not coll.is_dead() and self.current_animation == "fall": # for now this prevents multiple collisions
                        self.jump(0.5)
                        coll.bopped()

        # animate frames
        now = pg.time.get_ticks()
        if now - self.last_update > 60:  # 700 ms
            self.animate(dt)
            self.last_update = now  # Reset the timer


    def change_animation(self, next_animation_name, force=False):
        if self.current_animation != next_animation_name or force:
            self.frame_index = 0
            self.current_animation = next_animation_name


    def jump(self, strength_mod=1.0):
        self.velocity[1] = -self.jump_strength * strength_mod
        self.on_floor = False


    def animate(self, dt):
        self.frame_index += 1
        if self.frame_index > len(self.animations[self.current_animation]) - 1:
            self.frame_index = 0


    def render(self, surface, offset):
        adjusted_rect = self.rect().move(-offset.x, -offset.y)
        if self.direction == -1:
            surface.blit(pg.transform.flip(self.animations[self.current_animation][self.frame_index], True, False), adjusted_rect.move(self.render_offset[0], self.render_offset[1]))
        else:
            surface.blit(self.animations[self.current_animation][self.frame_index], adjusted_rect.move(self.render_offset[0], self.render_offset[1]))

        pg.draw.rect(surface, (0, 255, 0), adjusted_rect, 1)


    def __str__(self):
        return "Player"


    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RIGHT:
                self.inputs["right"] = True
            if event.key == pg.K_LEFT:
                self.inputs["left"] = True
            if event.key == pg.K_UP:
                self.inputs["up"] = True
            if event.key == pg.K_DOWN:
                self.inputs["down"] = True
            if event.key == pg.K_SPACE and self.on_floor:
                self.jump()
        if event.type == pg.KEYUP:
            if event.key == pg.K_RIGHT:
                self.inputs["right"] = False
            if event.key == pg.K_LEFT:
                self.inputs["left"] = False
            if event.key == pg.K_UP:
                self.inputs["up"] = False
            if event.key == pg.K_DOWN:
                self.inputs["down"] = False