import pygame
import math

class Camera:
  _instance = None

  # The __new__ method in Python is a static method responsible for creating and returning a new instance of a class. It is called before the __init__ method.
  def __new__(cls, width=None, height=None):
      if cls._instance is None:
          cls._instance = super(Camera, cls).__new__(cls)
          cls._instance.offset = pygame.Vector2(0, 0)
          cls._instance.width = width or 800
          cls._instance.height = height or 600
      return cls._instance

  def apply(self, target_rect):
      return target_rect.move(-self.offset.x, -self.offset.y)

  def update(self, target):
      cam_x = target.rect.centerx - self.width // 2
      cam_x = min(max(cam_x, 0), 600)
      self.offset.x = cam_x
      # self.offset.y = target.rect.centery - self.height // 2

  @staticmethod
  def get_instance():
      if Camera._instance is None:
          raise Exception("Camera has not been created yet!")
      return Camera._instance