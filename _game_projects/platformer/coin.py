import pygame as pg
from game_utils import load_animation_frames
import resources
from animatedsprite import AnimatedSprite


class Coin(AnimatedSprite):
  def __init__(self, x, y, *groups):
    super().__init__(*groups)
    image = resources.images["fg-tileset"].subsurface(pg.Rect(11 * 18, 7 * 18, 36, 18))
    animation = load_animation_frames(image, 0, 0, 18, 2)
    self.add_animation("default", animation)
    self.rect = pg.Rect(x, y, 18, 18)

  def set_position(self, x, y):
    self.rect.x = x
    self.rect.y = y