# Lesson 1 -
# Setting up and drawing to the screen

import pygame
import sys
from math import *

MAXSPEED = 50

pygame.init()
screen = pygame.display.set_mode((400,400))
clock = pygame.time.Clock()

triangle_points =  [(5,5), (20,10), (5, 15)]
car_group = pygame.sprite.Group()
car = pygame.sprite.Sprite(car_group)
car.image = pygame.Surface((20,20))
car.rect = car.image.get_rect()

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


running = True
while running == True:
  dt = min(clock.tick(60) / 1000.0, 0.05)
  
  screen.fill((0, 0, 0))
  
  # Keys
  key = pygame.key.get_pressed()
  if key[pygame.K_UP]:
    car_speed = max(car_speed + 0.05, MAXSPEED)
  else:
    car_speed *= 0.95
  if key[pygame.K_RIGHT]: 
      car_angle -= 2.0 * dt
  elif key[pygame.K_LEFT]:
      car_angle += 2.0 * dt

  
  pos_x += cos(car_angle) * dt * car_speed
  pos_y -= sin(car_angle) * dt * car_speed

  car.rect.centerx = round(pos_x)
  car.rect.centery = round(pos_y)

  # In your update loop
  rotated_points = [rotate_point(p, car_angle, (10, 10)) for p in triangle_points]

  # Clear and redraw the surface each frame
  car.image.fill((0, 0, 0, 0))  # transparent fill if using SRCALPHA
  pygame.draw.polygon(car.image, (255, 0, 0), rotated_points)
  car_group.draw(screen)

  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
        pygame.quit()
        sys.exit()