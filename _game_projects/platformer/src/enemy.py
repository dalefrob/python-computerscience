import pygame as pg
from pathlib import Path

from src.engine import Animation, AnimationPlayer
from src.physicsentity import *

path = Path(__file__).parent.resolve()

class Enemy(PhysicsEntity):
    IDLE = "idle"
    RUN = "run"
    HIT = "hit"
    DEAD = "dead"

    def __init__(self, game, pos):
        super().__init__(game, pos,  (26, 26))
        self.render_offset = [-3,-6]
        self.rotation = 0
        # states
        self.current_state = self.IDLE

        # animation setup
        idle = path / "../assets/Enemies/Mushroom/Idle (32x32).png"
        run = path / "../assets/Enemies/Mushroom/Run (32x32).png"
        hit = path / "../assets/Enemies/Mushroom/Hit.png"

        anim_player = AnimationPlayer()
        anim_player.add_animation("idle", Animation(idle, 14, 1))
        anim_player.add_animation("run", Animation(run, 16, 1))
        anim_player.add_animation("hit", Animation(hit, 5, 1, False), True)
        anim_player.on_animation_finished = self.on_animation_finished
        self.anim_player = anim_player

        self.direction = -1

        # attributes
        self.health = 3
        self.deadly_to_touch = True


    def ready(self):
        if self.current_state == self.RUN:
            self.anim_player.change_animation("run")


    def is_dead(self):
        return self.health <= 0


    def is_deadly_to_touch(self):
        if self.is_dead():
            return False
        return self.deadly_to_touch


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

        self.anim_player.update()


    def run(self, dt):
        if self.on_wall:
            self.direction *= -1


    def dead(self, dt):
        self.rotation += 1
        if self.pos.y < (pg.display.get_window_size()[1] * 2):
            del self


    def bopped(self):
        self.deadly_to_touch = False
        self.health -= 1
        if self.is_dead():
            self.current_state = self.DEAD
            self.playing = False
            self.velocity.y = -200
            self.disable_collision = True
            return
        self.anim_player.change_animation("hit", True)
        self.current_state = self.HIT


    def change_animation(self, next_animation_name, force=False):
        if self.current_animation != next_animation_name or force:
            self.frame_index = 0
            self.current_animation = next_animation_name


    def on_animation_finished(self):
        if self.anim_player.current_animation == "hit":
            self.deadly_to_touch = True
            self.current_state = self.RUN
            self.anim_player.change_animation("run")


    def render(self, surface, offset):
        adjusted_rect = self.rect().move(-offset.x, -offset.y)
        pg.draw.rect(surface, (0, 255, 0), adjusted_rect, 1)
        
        img_to_blit = self.anim_player.get_surface()
        img_to_blit = pg.transform.flip(img_to_blit, self.direction == 1, False)
        img_to_blit = pg.transform.rotate(img_to_blit, self.rotation)

        surface.blit(img_to_blit, adjusted_rect.move(self.render_offset[0], self.render_offset[1]))

        self.render_debug(surface, offset)


    def __str__(self):
        return "Mushroom"