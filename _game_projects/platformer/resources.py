import json
import pygame

images = {}
sounds = {}
other = {}

def load():
    global images, sounds, other
    images["fg-tileset"] = pygame.image.load("assets/tilemap_packed.png").convert_alpha()
    images["characters"] = pygame.image.load("assets/tilemap-characters_packed.png").convert_alpha()

    other["tileset_data"] = load_tileset_data_json( "assets/tileset_data.json")

def load_tileset_data_json(tileset_json_path):
     # load tile data
    file = open(tileset_json_path)
    json_data = json.load(file)
    file.close()
    return json_data