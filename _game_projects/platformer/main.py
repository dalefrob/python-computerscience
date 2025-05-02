import pygame as pg
import os
from coin import Coin
from game_utils import *
from player import Player
import resources
from tilemap import *

FPS = 60

# Construct the path dynamically
current_dir = os.path.dirname(__file__)

testmap = [
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0],
  [0,0,3,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,1,0,0,0,3,5,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  [3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,0],
]

class Game:
    def __init__(self):
        # Initialize your game systems here
        self.tilemap = Tilemap(...)  # Load your tilemap
        self.player = Player(x=100, y=100, width=50, height=50, game=self)

    def update(self, dt):
        # Update game systems (player, tilemap, etc.)
        self.player.update()
        
    def draw(self, screen):
        screen.fill("black")
        self.tilemap.draw(screen)
        self.player.draw(screen)



def main():
  pg.init()
  flags = pg.SCALED
  screen = pg.display.set_mode((320, 280), flags)
  pg.display.set_caption("World Map!")

  clock = pg.time.Clock()
  resources.load()


  # load resources
  player_spritesheet : pg.Surface = pg.image.load(os.path.join(current_dir, "assets/tilemap-characters_packed.png")).convert_alpha()
  tileset_texture = pg.image.load(os.path.join(current_dir, "assets/tilemap_packed.png")).convert_alpha()

  # initialize the map
  tileset_data = Tileset.load_tileset_data_json(os.path.join(current_dir, "assets/tileset_data.json"))
  tileset = Tileset(tileset_texture, tileset_data)
  tilemap = Tilemap(tileset, testmap)

  # init player
  player = Player(50, 50)
  player.add_animation("default", load_animation_frames(player_spritesheet, 0, 0, 24, 1))
  player.add_animation("walk", load_animation_frames(player_spritesheet, 0, 0, 24, 2))
  player.add_animation("jump", load_animation_frames(player_spritesheet, 24, 0, 24, 1))
  player_group = pg.sprite.GroupSingle(player)

  # coin
  coins = pg.sprite.Group()
  coin = Coin(3*18, 5*18)
  coins.add(coin)

  running = True
  while running:
    dt = min(clock.tick(60) / 1000.0, 0.05)

    screen.fill("black")
    tilemap.draw(screen)

    player.handle_input(pg.key.get_pressed())
    player.update(dt)
    coin.update(dt)

    # check collisions
    response = resolve_tilemap_collision(player.rect, tilemap)
    if response:
        push_vector, normal = response
        # Move the player out of collision
        player.rect.x += push_vector.x
        player.rect.y += push_vector.y

        # Cancel velocity in the direction of collision
        if normal.x != 0:
          player.velocity.x = 0
        if normal.y != 0:
          if normal.y < 0:
             player.on_ground = True 
          player.velocity.y = 0
    
    # coin collision
    coll_object : Coin = pg.sprite.spritecollideany(player, coins)
    if coll_object:
       print(coll_object)
       coll_object.kill()
       del coll_object

    player_group.draw(screen)

    pg.display.flip()

    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        running = False



if __name__ == "__main__":
  main()