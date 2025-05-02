import json
import pygame
import os

images = {}
sounds = {}
other = {}

def load():
    current_dir = os.path.dirname(__file__)
    global images, sounds, other
    images["fg-tileset"] = pygame.image.load(os.path.join(current_dir, "assets/tilemap_packed.png")).convert_alpha()
    images["characters"] = pygame.image.load(os.path.join(current_dir, "assets/tilemap-characters_packed.png")).convert_alpha()
    sounds["jump"] = pygame.mixer.Sound(os.path.join(current_dir, "assets/jump1.ogg"))
    sounds["pickup"] = pygame.mixer.Sound(os.path.join(current_dir, "assets/pickup1.ogg"))
    other["tileset_data"] = load_tileset_data_json(os.path.join(current_dir, "assets/tileset_data.json"))

def load_tileset_data_json(tileset_json_path):
     # load tile data
    file = open(tileset_json_path)
    json_data = json.load(file)
    file.close()
    return json_data