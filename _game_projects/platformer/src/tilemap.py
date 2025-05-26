import pygame as pg
import json
from pathlib import Path

path = Path(__file__).parent.resolve()


class Tile():
    """ 
    Basic structure to hold tile info 
    """
    TILE_SOLID = 0
    TILE_PLATFORM = 1
    
    def __init__(self, coord, size, src_coord):
        self.coord = coord
        self.size = size
        self.src_coord = src_coord
        self.collision = 0
    
    def get_rect(self):
        rect = pg.Rect(self.coord[0] * self.size[0], self.coord[1] * self.size[1], self.size[0], self.size[1])
        return rect


class TilemapLayer():
    def __init__(self, map_width, map_height, cell_size):
        
        # size
        self.layer_id = 0
        self.cell_size = cell_size
        self.width = map_width
        self.height = map_height
        self.surface = pg.Surface((map_width, map_height))

        # tiles
        self.map_settings = load_map_settings("testmap")
        self.tiles_atlas = load_tilesheet()  # TODO -- Load this from the ldtk settings
        self.tiles = load_level("Level_0")
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
    

class Level():
    """
    A ldtk level that contains the tilemap, entity locations. 
    """
    def __init__(self, game, level_name="Level_0"):
        self.game = game
        
        self.tilemap_layers = []
        self.entity_layers = []

        _result = {}
        json_path = path / f"../assets/Maps/testmap/{level_name}.ldtkl"
        with open(json_path, "r") as read_file: # Open the file, read it and clsoe the file
            _result = json.load(read_file)
        
        self.px_width = _result["pxWid"]
        self.px_height = _result["pxHei"]

        # Load the tilemap layers
        for layer_instance_dict in _result["layerInstances"]:
            layer = None
            match layer_instance_dict["__type"]:
                case "Tiles":
                    layer = self.load_tilemap_layer(layer_instance_dict)
                    self.tilemap_layers.append(layer)
                case "Entities":
                    layer = self.load_entity_layer(layer_instance_dict)
                    self.entity_layers.append(layer)

        print(f"Level '{level_name}' loaded")    


    def get_fg_layer(self):
        return self.tilemap_layers[0]


    def load_tilemap_layer(self, layer_instance_dict) -> TilemapLayer:
        cell_size = 16
        tilemap_layer = TilemapLayer(self.px_width, self.px_height, cell_size)
        _tiles = {}
        grid_tiles = layer_instance_dict['gridTiles']
        for i in grid_tiles:
            screen_coord = i["px"]
            src_coord = i["src"] 
            key = (screen_coord[0] // 16, screen_coord[1] // 16)
            value = (src_coord[0] // 16, src_coord[1] // 16)
            # Set up tile
            tile = Tile(key, (16, 16), value)
            tile.collision = 0 # self.get_tile_collsion()
            _tiles[key] = tile
        tilemap_layer.tiles = _tiles
        return tilemap_layer


    def load_entity_layer(self, layer_instance_dict):
        entities = []
        for e in layer_instance_dict["entityInstances"]:
            entity = {
                "name": e["__identifier"],
                "world_pos": e["px"] 
            }
            entities.append(entity)
        return entities


    def render(self, surface, offset):
        for layer in self.tilemap_layers:
            assert isinstance(layer, TilemapLayer)
            layer.render(surface, offset)
            


class Tileset():
    def __init__(self):
        pass


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


def load_map_settings(map_name):
    """
    Loads the map/world settings from a 'ldtk' file
    """
    json_path = path / f"../assets/Maps/{map_name}.ldtk"
    with open(json_path, "r") as read_file:
        result = json.load(read_file)
    return result


def load_tilemap_layer_OB(level_data):
    map_tiles = {}
    grid_tiles = level_data['layerInstances'][0]['gridTiles']
    for i in grid_tiles:
        screen_coord = i["px"]
        src_coord = i["src"] 
        key = (screen_coord[0] // 16, screen_coord[1] // 16)
        value = (src_coord[0] // 16, src_coord[1] // 16)
        # Set up tile
        tile = Tile(key, (16, 16), value)
        tile.collision = 0 # self.get_tile_collsion()
        map_tiles[key] = tile
    return map_tiles



def load_level(level_name):
    """
    Loads a full level from a 'ldtkl' file - note the final 'l'
    """
    map_tiles = {}
    json_path = path / f"../assets/Maps/testmap/{level_name}.ldtkl"

    with open(json_path, "r") as read_file: # Open the file, read it and clsoe the file
        result = json.load(read_file)

    map_tiles = load_tilemap_layer_OB(result)

    return map_tiles
