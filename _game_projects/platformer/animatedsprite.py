import pygame as pg


class AnimatedSprite(pg.sprite.Sprite):
  """
  An animated sprite that holds more than one set of animation frames.
  """
  def __init__(self, position=(0,0), inital_frames=None, frame_size=(24, 24)):
    super().__init__()
    self.position = position
    self.rect = pg.Rect(position, frame_size)

    self.animations = {}
    self.current_animation = ""
    self.current_frame = 0
    self.animation_speed = 0.2
    self.flip_h = False
    self.draw_offset = (0,0)

    if not inital_frames:
      raise("No initial animation frames!")
    
    self.add_animation("default", inital_frames)
    self.image = inital_frames[0]


  def add_animation(self, alias, animation_frames):
    self.animations[alias] = animation_frames
    if len(self.animations) == 1:
      self.current_animation = alias


  def change_animation_to(self, alias, force=False):
    if self.current_animation == alias and not force:
      return # Do not change to the same animation
    if not self.animations[alias]:
      print(f"Animation not found: {alias}")
      return

    self.current_frame = 0
    self.current_animation = alias


  def update(self, dt):
    self._animate(dt)
    orig_image : pg.Surface = self.animations[self.current_animation][self.current_frame]
    self.image = pg.transform.flip(orig_image, self.flip_h, False)


  def _animate(self, dt):
    # update the frame
    self.animation_speed -= dt
    if self.animation_speed <= 0:
      self.animation_speed = 0.25
      self.current_frame += 1
      if self.current_frame >= len(self.animations[self.current_animation]):
        self.current_frame = 0


  def draw_with_offset(self, screen):
    # orig_image : pg.Surface = self.animations[self.current_animation][self.current_frame]
    # self.image = pg.transform.flip(orig_image, self.flip_h, False)
    screen.blit(self.image,  self.rect.move(self.draw_offset))