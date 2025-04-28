import pygame as pg
import json



class Tilemap:
  def __init__(self, tileset, map_data=None, width=10, height=10):
    self.tileset = tileset

    if map_data:
        self.tiles = map_data
        width = len(map_data)
        height = len(map_data[0])
    else:
      self.tiles = [[0 for _ in range(width)] for _ in range(height)]

    self.surf = pg.Surface((width * self.tileset.tilesize, height * self.tileset.tilesize))
    self.surf.fill("black")
    self.surf.set_colorkey("black")


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
    screen.blit(self.surf, (0, 0))


  def get_tile_at(self, x, y):
    if 0 <= x <= len(self.tiles) and 0 <= y <= len(self.tiles[x]): 
      return self.tiles[y][x]
    return 0


class Tile:
  def __init__(self, image, data = {}):
    self.image = image
    self.data = data



class Tileset:
  def __init__(self, tileset_path, tileset_json_path):
    # init vars
    self.tiles = {}
    self.tile_data = {}
    # load texture
    self.texture = pg.image.load(tileset_path).convert_alpha()
    # load tile data
    file = open(tileset_json_path)
    json_data = json.load(file)

    self.tilesize = json_data["tilesize"]
    for id in json_data["tiles"]:
      tile_id = int(id)
      props = json_data["tiles"][id]
      self.add_tile(tile_id, pg.Rect(props["x"], props["y"], self.tilesize, self.tilesize), props["data"])



  def add_tile(self, tile_id, region_rect, data=None):
    # Create a new tile image from the texture using the specified region
    image = self.texture.subsurface(region_rect)
    tile = Tile(image, data)
    self.tiles[tile_id] = tile


  def get_tile_by_id(self, tile_id) -> Tile:
    return self.tiles[tile_id]




class Shape:
  def __init__(self, position, points=[]):
    self.position = position
    self.points = points
  
  


def is_point_in_polygon(x, y, polygon):
  """
  Algorithm to check if a point is within a polygon by raycasting
  a horizontal line across the polygon and counting the intersections.
  """
  num = len(polygon)
  j = num - 1
  inside = False

  for i in range(num):
      xi, yi = polygon[i] # point a
      xj, yj = polygon[j] # point a - 1 (previous point)
      if ((yi > y) != (yj > y)):
          x_intersect = (xj - xi) * (y - yi) / (yj - yi) + xi
          if x < x_intersect:
              inside = not inside
      j = i

  return inside



shapes = {
  "full": [(0,0), (1,0), (1,1), (0,1)],
  "left_slope": [(0,1), (1,0), (1,1)],
  "right_slope": [(1,0), (1,1), (0,1)]
}