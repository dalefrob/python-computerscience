import pygame as pg
from game_utils import load_animation_frames
import resources
from animatedsprite import AnimatedSprite


class Coin(AnimatedSprite):
  def __init__(self, position, *groups):
    image = resources.images["fg-tileset"].subsurface(pg.Rect(11 * 18, 7 * 18, 36, 18))
    animation = load_animation_frames(image, 0, 0, 18, 2)
    super().__init__(position, animation)
    x, y = position
    self.rect = pg.Rect(x, y, 18, 18)

  def set_position(self, x, y):
    self.rect.x = x
    self.rect.y = y