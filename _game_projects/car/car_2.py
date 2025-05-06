# Lesson 2 -
# Loading resources

import pygame
import sys, os
from math import *

MAXSPEED = 10

# Load resources
dir_path = os.path.dirname(os.path.realpath(__file__))
car_image = pygame.image.load(dir_path + "/assets/car_red_small_5.png")

pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

car_group = pygame.sprite.Group()
car = pygame.sprite.Sprite(car_group)
original_image = pygame.transform.scale(car_image, (39/2, 65/2))
original_pivot = [39/4, 65/4]
car.image = original_image

pos_x = 200.0
pos_y = 200.0
car_speed = 0.0
car_angle = 0.0

def rotate_point(point, angle, center):
    angle = -angle # Account for the screen coordinates starting from top left instead of regular x,y
    x, y = point
    cx, cy = center

    # Translate to origin
    x -= cx
    y -= cy

    # Rotate
    x_rot = x * cos(angle) - y * sin(angle)
    y_rot = x * sin(angle) + y * cos(angle)

    # Translate back
    return (x_rot + cx, y_rot + cy)

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image,rot_rect

running = True
while running == True:
  dt = min(clock.tick(60) / 1000.0, 0.05)
  
  screen.fill((0, 0, 0))
  
  # Keys
  key = pygame.key.get_pressed()
  if key[pygame.K_UP]:
    car_speed = max(car_speed + 0.5, MAXSPEED)
  elif key[pygame.K_DOWN]:
    car_speed = max(car_speed - 1, -MAXSPEED * 0.75)
  else:
    car_speed *= 0.975
  if key[pygame.K_RIGHT]: 
      car_angle -= 2.0 * dt
  elif key[pygame.K_LEFT]:
      car_angle += 2.0 * dt

  
  pos_x += cos(car_angle) * dt * car_speed
  pos_y -= sin(car_angle) * dt * car_speed

  car.image = pygame.transform.rotate(original_image, (car_angle - (pi/2)) * (180/pi))
  offset = pygame.Vector2(round(pos_x), round(pos_y))
  car.rect = car.image.get_rect(center=original_pivot + offset)

  #car.rect.centerx = round(pos_x)
  #car.rect.centery = round(pos_y)

  car_group.draw(screen)

  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        sys.exit()