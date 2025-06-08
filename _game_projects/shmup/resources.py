import pygame as pg
from pathlib import Path

SCREENWIDTH = 280
SCREENHEIGHT = 540

# Load resources
path = Path(__file__).parent.resolve()
assets = {}

def load_resources():
    assets["ship_sheet"] = pg.image.load(path / "assets/ships_packed.png").convert_alpha()
    assets["tile_sheet"] = pg.image.load(path / "assets/tiles_packed.png").convert_alpha()
    assets["shoot_sound"] = pg.mixer.Sound(path / "assets/laserRetro_000.ogg")

ship_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()

