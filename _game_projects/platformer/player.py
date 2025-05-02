import pygame as pg
from camera import Camera
from animatedsprite import AnimatedSprite
import resources

GRAVITY = 16.0


class Player(AnimatedSprite):
  def __init__(self, position, initial_frames):
    super().__init__(position, initial_frames)

    self.velocity = pg.Vector2(0, 0)
    self.speed = 30.0
    self.on_ground = False

    self.rect.size = (18,18)
    self.draw_offset = (-2,-4)

    self.camera = Camera.get_instance()


  def update(self, dt):
    super().update(dt)
    # add gravity
    self.velocity.y += GRAVITY * dt
    self._move(dt)
    
    if not self.on_ground:
      self.change_animation_to("jump")
    else:
      if abs(self.velocity.x) > 0 and self.on_ground:
        self.change_animation_to("walk")
      else:
        self.change_animation_to("default")


  def jump(self):
    pg.mixer.Sound.play(resources.sounds["jump"])
    self.velocity.y = -7.8
    self.on_ground = False


  def _move(self, dt):
    self.rect.x += self.velocity.x * self.speed * dt
    self.rect.y += self.velocity.y * self.speed * dt


  def handle_input(self, keys):
    if keys[pg.K_SPACE] and self.on_ground:
      self.jump()

    if keys[pg.K_RIGHT]:
      self.flip_h = True
      self.velocity.x = 2
    elif keys[pg.K_LEFT]:
      self.flip_h = False
      self.velocity.x = -2
    else:
      self.velocity.x = 0

  def draw_with_offset(self, screen):
    # orig_image : pg.Surface = self.animations[self.current_animation][self.current_frame]
    # self.image = pg.transform.flip(orig_image, self.flip_h, False)
    screen.blit(self.image,  self.camera.apply(self.rect.move(self.draw_offset)))