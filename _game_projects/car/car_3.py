# Lesson 3 -
# Drawing a track

import pygame
import sys, os
from math import *

TILESIZE = 128
GRASS_GREEN = (30, 150, 50)

class Car(pygame.sprite.Sprite):
  def __init__(self, x, y, angle=0.0, *groups):
    super().__init__(*groups)
    self.position = pygame.Vector2(x, y)
    self.orig_image = pygame.image.load(dir_path + "/assets/car_red_small_5.png")
    self.original_pivot = [39/4, 65/4]

    self.max_speed = 10.0
    self.speed = 0.0
    self.angle = angle
  
  def update(self, dt):
    # Keys
    self.do_input(dt)
    
    self.position.x += cos(self.angle) * dt * self.speed
    self.position.y -= sin(self.angle) * dt * self.speed

    self.set_image()

  def set_image(self):
      self.image = pygame.transform.rotozoom(self.orig_image, (self.angle - (pi/2)) * (180/pi), 0.5)
      offset = pygame.Vector2(round(self.position.x), round(self.position.y))
      self.rect = self.image.get_rect(center=self.original_pivot + offset)

  def do_input(self, dt):
      key = pygame.key.get_pressed()
      if key[pygame.K_UP]:
        self.speed = max(self.speed + 0.5, self.max_speed)
      elif key[pygame.K_DOWN]:
        self.speed = max(self.speed - 1, -self.max_speed * 0.75)
      else:
        self.speed *= 0.975
      if key[pygame.K_RIGHT]: 
          self.angle -= 2.0 * dt
      elif key[pygame.K_LEFT]:
          self.angle += 2.0 * dt

# Load resources
dir_path = os.path.dirname(os.path.realpath(__file__))
car_image = pygame.image.load(dir_path + "/assets/car_red_small_5.png")
track_pieces = {
  1: pygame.image.load(dir_path + "/assets/road_asphalt01.png"), # vertical
  2: pygame.image.load(dir_path + "/assets/road_asphalt02.png"), # horizontal
  3: pygame.image.load(dir_path + "/assets/road_asphalt03.png"), # topleft
  5: pygame.image.load(dir_path + "/assets/road_asphalt05.png"), # topright
  39: pygame.image.load(dir_path + "/assets/road_asphalt39.png"), # bottomleft
  41: pygame.image.load(dir_path + "/assets/road_asphalt41.png"), # bottomright
  42: pygame.image.load(dir_path + "/assets/road_asphalt42.png"), # verticalstart
}

def draw_track(screen : pygame.Surface, id : int, cell : tuple):
  screen.blit(track_pieces[id], (cell[0] * TILESIZE, cell[1] * TILESIZE))


# Initalize
pygame.init()
screen = pygame.display.set_mode((5 * TILESIZE, 5 * TILESIZE))
clock = pygame.time.Clock()

car_group = pygame.sprite.Group()
car_start = pygame.Vector2(4 * TILESIZE, 2 * TILESIZE) + pygame.Vector2(TILESIZE / 2)
car = Car(car_start.x, car_start.y, pi/2, car_group)

running = True
while running == True:
  dt = min(clock.tick(60) / 1000.0, 0.05)
  
  screen.fill(GRASS_GREEN)
  # Straights
  draw_track(screen, 2, (1,0))
  draw_track(screen, 2, (2,0))
  draw_track(screen, 2, (3,0))
  draw_track(screen, 1, (0,1))
  draw_track(screen, 1, (0,2))
  draw_track(screen, 1, (0,3))
  draw_track(screen, 1, (4,1))
  draw_track(screen, 42, (4,2))
  draw_track(screen, 1, (4,3))
  draw_track(screen, 2, (1,4))
  draw_track(screen, 2, (2,4))
  draw_track(screen, 2, (3,4))
  # Corners
  draw_track(screen, 3, (0,0))
  draw_track(screen, 5, (4,0))
  draw_track(screen, 39, (0,4))
  draw_track(screen, 41, (4,4))

  car_group.update(dt)
  car_group.draw(screen)

  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        sys.exit()