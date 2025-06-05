from pathlib import Path
import pygame as pg
import random

SCREENWIDTH = 280
SCREENHEIGHT = 540

class Ship(pg.sprite.Sprite):
    def __init__(self, image : pg.Surface, *groups):
        super().__init__(*groups)
        self.image = image
        self.rect = image.get_rect(center=(140, 500))


class Star():
    def __init__(self, x, y, size = 4):
        self.position = pg.Vector2(x, y)
        self.surface = pg.Surface((size,size))
        self.surface.set_colorkey((0,0,0))
        if size <= 2:
            self.surface.fill((255, 200, random.randint(0,255)))
        else:
            pg.draw.circle(self.surface, (255,255,random.randint(100,255)), (size/2,size/2), size / 3)
        self.speed = size * 4
    
    def get_rect(self):
        return pg.Rect(self.position.x, self.position.y, 2, 2)
    
    def update(self, dt):
        self.position.y += self.speed * dt
        if self.position.y > SCREENHEIGHT:
            self.position.y = 0

    def render(self, screen : pg.Surface):
        screen.blit(self.surface, self.get_rect())


pg.init()
screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pg.Clock()

# Load resources
path = Path(__file__).parent.resolve()
ship_sheet = pg.image.load(path / "ships_packed.png").convert_alpha()
tile_sheet = pg.image.load(path / "tiles_packed.png").convert_alpha()
ship_image = ship_sheet.subsurface(pg.Rect(0, 0, 32, 32))

stars = []
sizes = [1, 2, 4]
for _ in range(100):
    star = Star(random.randint(0, SCREENWIDTH), random.randint(0, SCREENHEIGHT), random.choice(sizes))
    stars.append(star)


allsprites = pg.sprite.Group()
ship = Ship(ship_image, allsprites)

running = True
while running:
    dt = clock.tick(60) / 1000

    screen.fill((0, 0, 0))

    for s in stars:
        s.update(dt)
        s.render(screen)

    allsprites.draw(screen)

    pg.display.flip()
    events = pg.event.get()
    for e in events:
        if e.type == pg.QUIT:
            running = False

pg.quit()