import pygame as pg
import json
from pathlib import Path

path = Path(__file__).parent.resolve()

TILE_NONSOLID = 0
TILE_SOLID = 1
TILE_PLATFORM = 2

class Tile():
    """ Basic structure to hold tile info """
    def __init__(self, coord, size, src_coord):
        self.coord = coord
        self.size = size
        self.src_coord = src_coord
        self.solidarity = TILE_SOLID
    
    def get_rect(self):
        rect = pg.Rect(self.coord[0] * self.size[0], self.coord[1] * self.size[1], self.size[0], self.size[1])
        return rect


class Tilemap():
    def __init__(self, game, map_width, map_height, cell_size):
        self.game = game
        # size
        self.cell_size = cell_size
        self.width = map_width
        self.height = map_height
        self.surface = pg.Surface((cell_size * map_width, cell_size * map_height))

        # tiles
        self.tiles_atlas = load_tilesheet()
        self.tiles = load_ldtk_map()
        # test
        self.platforms = [(2,9), (3,9), (4,9)]

        # Debug
        self.render_coords = False
        self.debug_rect = False
    

    def get_neighbor_rects(self, map_coord, debug = False):
        rects = []
        for offset in neighbor_offsets:
            test_coord = (map_coord[0] + offset[0], map_coord[1] + offset[1])
            #print(test_coord)
            if test_coord in self.tiles:
                rect = self.tiles[test_coord].get_rect()
                # rect = pg.Rect(test_coord[0] * self.cell_size, test_coord[1] * self.cell_size, self.cell_size, self.cell_size)
                rects.append(rect) # Add whether its a platform or not
            if debug and len(rects) > 0:
                dbrect = rects[0].copy()
                self.debug_rect = dbrect.unionall(rects)
        return rects

    # TODO -  Get the tiles adjacent
    def get_neighbor_tiles(self, map_coord):
        tiles = []
        for offset in neighbor_offsets:
            test_coord = (map_coord[0] + offset[0], map_coord[1] + offset[1])
            if test_coord in self.tiles:
                tile = self.tiles[test_coord]
                tiles.append(tile)
        return tiles


    def map_to_world(self, map_coord):
        return (map_coord[0] * self.cell_size, map_coord[1] * self.cell_size)


    def world_to_map(self, screen_coord):
        return (int(screen_coord[0] // self.cell_size), int(screen_coord[1] // self.cell_size) + 1)


    def render(self, surface, offset=[0,0]):
        for coordinate, tile_obj in self.tiles.items():
            tile = self.tiles_atlas[tile_obj.src_coord]
            assert isinstance(tile, pg.Surface)
            surface.blit(tile, pg.Rect(self.map_to_world(coordinate), (16, 16)).move(-offset[0], -offset[1]))
        if self.render_coords:
            for col in range(self.width):
                for row in range(self.height):
                    # +1 in cell size allows the rects to draw in a grid
                    rect = pg.Rect(col * self.cell_size, row * self.cell_size, self.cell_size + 1, self.cell_size + 1).move(-offset[0], -offset[1])
                    pg.draw.rect(surface, (180, 180, 0), rect, 1)
        if self.debug_rect:
            pg.draw.rect(surface, (100, 100, 0), self.debug_rect.move(-offset[0], -offset[1]))


neighbor_offsets = [
    [0,0],
    [-1, 0],
    [-1, -1],
    [0, -1],
    [1, 1],
    [1, 0],
    [1, -1],
    [0, -1],
    [-1, -1],
    [-1, -2],
    [0, -2],
    [1, -2]
]


def load_tilesheet(tilesize = 16):
    tilesheet_path = path / "../assets/Terrain/Terrain (16x16).png"
    image = pg.image.load(tilesheet_path)
    image_width, image_height = image.get_size()
    tiles_across = image_width // tilesize
    tiles_down = image_height // tilesize
    atlas = {}
    for row in range(tiles_down):
        for col in range(tiles_across):
            subsurf = image.subsurface((col * tilesize, row * tilesize), (tilesize, tilesize))
            atlas[col, row] = subsurf
    return atlas


def load_ldtk_map():
    map_tiles = {}
    json_path = path / "../assets/Maps/testmap/Level_0.ldtkl"
    with open(json_path, "r") as read_file:
        result = json.load(read_file)
        grid_tiles = result['layerInstances'][0]['gridTiles']
        for i in grid_tiles:
            screen_coord = i["px"]
            src_coord = i["src"] 
            key = (screen_coord[0] // 16, screen_coord[1] // 16)
            value = (src_coord[0] // 16, src_coord[1] // 16)
            # Set up tile
            tile = Tile(key, (16, 16), value)

            map_tiles[key] = tile
    return map_tiles
