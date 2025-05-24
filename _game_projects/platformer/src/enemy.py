import pygame as pg
from pathlib import Path

from src.physicsentity import *

path = Path(__file__).parent.resolve()

class Enemy(PhysicsEntity):
    IDLE = "idle"
    RUN = "run"
    HIT = "hit"
    DEAD = "dead"

    def __init__(self, game, pos, size):
        super().__init__(game, pos, size)
        self.render_offset = [-3,-6]
        self.rotation = 0
        # states
        self.current_state = self.IDLE

        # animation setup
        idle = path / "../assets/Enemies/Mushroom/Idle (32x32).png"
        run = path / "../assets/Enemies/Mushroom/Run (32x32).png"
        hit = path / "../assets/Enemies/Mushroom/Hit.png"

        self.animations = {
            "idle": load_animation_frames(idle, 14, 1),
            "run": load_animation_frames(run, 16, 1),
            "hit": load_animation_frames(hit, 5, 1)
        }
        
        self.current_animation = "idle"
        self.playing = True
        self.last_update = 0
        self.frame_index = 0
        self.direction = -1

        # attributes
        self.health = 3


    def is_dead(self):
        return self.health <= 0


    def update(self, dt):
        self.velocity[1] += GRAVITY # Add gravity

        # run a method based on state
        if hasattr(self, self.current_state):
            getattr(self, self.current_state)(dt)

        match self.current_state:
            case self.IDLE | self.HIT:
                self.velocity[0] = 0
            case self.RUN:
                self.velocity[0] = self.direction * self.speed

        self.move_and_collide(dt)

        # animate frames
        now = pg.time.get_ticks()
        if now - self.last_update > 60 and self.playing:  # 700 ms
            self.animate(dt)
            self.last_update = now  # Reset the timer


    def run(self, dt):
        if self.on_wall:
            self.direction *= -1


    def dead(self, dt):
        self.rotation += 1
        if self.pos.y < (pg.display.get_window_size()[1] * 2):
            del self


    def bopped(self):
        self.health -= 1
        if self.is_dead():
            self.current_state = self.DEAD
            self.playing = False
            self.velocity.y = -200
            self.disable_collision = True
            return
        self.change_animation("hit")
        self.current_state = self.HIT


    def change_animation(self, next_animation_name):
        if self.current_animation != next_animation_name:
            self.frame_index = 0
            self.current_animation = next_animation_name


    def on_animation_ended(self):
        if self.current_animation == "hit":
            self.current_state = self.RUN
            self.change_animation("run")


    def animate(self, dt):
        self.frame_index += 1
        if self.frame_index > len(self.animations[self.current_animation]) - 1:
            self.on_animation_ended()
            self.frame_index = 0


    def render(self, surface, offset):
        adjusted_rect = self.rect().move(-offset.x, -offset.y)
        pg.draw.rect(surface, (0, 255, 0), adjusted_rect, 1)
        img_to_blit = self.animations[self.current_animation][self.frame_index]
        img_to_blit = pg.transform.flip(img_to_blit, self.direction == 1, False)
        img_to_blit = pg.transform.rotate(img_to_blit, self.rotation)
        surface.blit(img_to_blit, adjusted_rect.move(self.render_offset[0], self.render_offset[1]))

        self.render_debug(surface, offset)

    def __str__(self):
        return "Mushroom"