import random
import pygame as pg
import os
from tilemap import *

FPS = 60

# Construct the path dynamically
current_dir = os.path.dirname(__file__)

testmap = [
  [0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,2,2,2],
  [0,0,3,5,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0],
  [0,1,0,0,0,3,5,0,0],
  [0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0],
  [3,4,4,4,4,4,4,4,5],
]


class Player(pg.sprite.Sprite):
  def __init__(self, x, y, *groups):
    super().__init__(*groups)
    self.position = pg.Vector2(x, y)
    # load image
    self.animation = self.load_animation()
    self.current_frame = 0
    self.rect = self.animation[self.current_frame].get_rect()

    self.anim_speed = 0.25
  

  def load_animation(self):
    full_image : pg.Surface = pg.image.load(os.path.join(current_dir, "assets/tilemap-characters_packed.png")).convert_alpha()
    frames = []
    for i in range(2):
      frame = full_image.subsurface(i * 24, 0, 24, 24)
      frames.append(frame)
    return frames


  def update(self, dt):
    self.anim_speed -= dt
    if self.anim_speed <= 0:
      self.anim_speed = 0.25
      self.current_frame += 1
      if self.current_frame >= len(self.animation):
        self.current_frame = 0


  def draw(self, screen):
    screen.blit(self.animation[self.current_frame], self.rect)


  def handle_input(self, keys):
    if keys[pg.K_RIGHT]: 
      self.rect.x += 2 
    elif keys[pg.K_LEFT]:
      self.rect.x -= 2


def main():
  pg.init()
  screen = pg.display.set_mode((400, 400))
  pg.display.set_caption("World Map!")

  clock = pg.time.Clock()

  # initialize the map
  tileset_path = os.path.join(current_dir, "assets/tilemap_packed.png")
  tilest_data_path = os.path.join(current_dir, "assets/tileset_data.json")
  tileset = Tileset(tileset_path, tilest_data_path)
  tilemap = Tilemap(tileset, testmap)

  # init player
  player = Player(50, 50)

  running = True
  while running:
    dt = clock.tick(FPS) / 1000.0

    screen.fill("black")
    tilemap.draw(screen)

    player.handle_input(pg.key.get_pressed())
    player.update(dt)
    player.draw(screen)

    pg.display.flip()

    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        running = False



if __name__ == "__main__":
  main()