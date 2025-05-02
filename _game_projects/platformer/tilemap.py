import pygame as pg
import json

from game_utils import *
from camera import Camera


class Tilemap:
  def __init__(self, tileset, map_data=None, width=10, height=10):
    self.tileset = tileset

    if map_data:
        self.tiles = map_data
        height = len(map_data)
        width = len(map_data[0])
    else:
      self.tiles = [[0 for _ in range(width)] for _ in range(height)]

    self.surf = pg.Surface((width * self.tileset.tilesize, height * self.tileset.tilesize))
    self.surf.fill("black")
    self.surf.set_colorkey("black")

    self.camera = Camera.get_instance()


  def get_tilesize(self):
    return self.tileset.tilesize


  def draw(self, screen):
    tilesize = self.tileset.tilesize
    for y in range(len(self.tiles)):
      for x in range(len(self.tiles[y])):
        if self.tiles[y][x] != 0:
          tile_id = self.tiles[y][x]
          tile : Tile = self.tileset.get_tile_by_id(tile_id)
          if tile:
            self.surf.blit(tile.image, (x * tilesize, y * tilesize))

    # draw the surface on the screen
    rect = pg.Rect(0,0, self.camera.width, self.camera.height)
    screen.blit(self.surf, self.camera.apply(rect))


  def world_to_map(self, x, y):
    return (x // self.get_tilesize(), y // self.get_tilesize())


  def map_to_world(self, x, y):
    return pg.Vector2(self.get_tilesize() * x, self.get_tilesize() * y)


  def get_tile_id_at(self, x, y):
    if 0 <= y < len(self.tiles) and 0 <= x < len(self.tiles[y]): 
      return self.tiles[y][x]
    return 0


class Tile:
  def __init__(self, image : pg.Surface, tile_data = {}):
    self.image = image
    self.data = tile_data
    self.rect = image.get_rect()



class Tileset:
  def __init__(self, texture : pg.Surface, tileset_data):
    # init vars
    self.tiles = {}
    self.tile_data = {}
    # load texture
    self.texture = texture
   
    self.tilesize = tileset_data["tilesize"]
    for id in tileset_data["tiles"]:
      tile_id = int(id)
      props = tileset_data["tiles"][id]
      self.add_tile(tile_id, pg.Rect(props["x"], props["y"], self.tilesize, self.tilesize), props["data"])



  def add_tile(self, tile_id, region_rect, data=None):
    # Create a new tile image from the texture using the specified region
    image = self.texture.subsurface(region_rect)
    tile = Tile(image, data)
    self.tiles[tile_id] = tile


  def get_tile_by_id(self, tile_id) -> Tile:
    return self.tiles[tile_id]


  @staticmethod
  def load_tileset_data_json(tileset_json_path):
     # load tile data
    file = open(tileset_json_path)
    json_data = json.load(file)
    file.close()
    return json_data




class Shape:
  def __init__(self, position, points=[]):
    self.position = position
    self.points = points
  
shapes = {
  "full": [(0,0), (1,0), (1,1), (0,1)],
  "left_slope": [(0,1), (1,0), (1,1)],
  "right_slope": [(1,0), (1,1), (0,1)]
}