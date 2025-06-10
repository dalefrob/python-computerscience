import pygame as pg
import random
from resources import *
from entities import PlayerShip, EnemyShip, Timer

class Starfield():
    """
    A generated static starfield background
    """
    def __init__(self, size : tuple, stars : int):
        surf = pg.Surface(size)
        surf.fill((0, 0, 0))
        for _ in range(stars):
            point = (random.randint(0, size[0]), random.randint(0, size[1]))
            surf.set_at(point, (100, 100, 100))
        self.surf = surf
    
    def render(self, screen : pg.Surface):
        screen.blit(self.surf)

class Star():
    def __init__(self, x, y, size = 4):
        self.position = pg.Vector2(x, y)
        self.surface = pg.Surface((size,size))
        self.surface.set_colorkey((0,0,0))
        if size <= 2:
            rg = random.randint(180,220)
            self.surface.fill((rg, rg * random.random(), random.randint(0,255)))
        else:
            rg = random.randint(100,200)
            pg.draw.circle(self.surface, (rg, rg, random.randint(180,200)), (size/2,size/2), size / 3)
        self.speed = size * 4
    
    def get_rect(self):
        return pg.Rect(self.position.x, self.position.y, 2, 2)
    
    def update(self, dt):
        self.position.y += self.speed * dt
        if self.position.y > SCREENHEIGHT:
            self.position.y = 0

    def render(self, screen : pg.Surface):
        screen.blit(self.surface, self.get_rect())

class WaveManager():
    """
    Handles the spawning of enemies in waves.
    """
    def __init__(self):
        self.timer = Timer(1000, self.on_timer_tick, True, True)
        self.ticks : int = 0
        self.seq = {
            1: [("EnemyShip", (80, 0), {}), ("EnemyShip", (120, 0), {}), ("EnemyShip", (160, 0), { "flipped": True }), ("EnemyShip", (200, 0), { "flipped": True })], # At 5 seconds, spawn an enemy ship at (40, 0)
            5: [("EnemyShip", (200, 0), { "flipped": True })], # At 5 seconds, spawn an enemy ship at (40, 0)
            8: [("EnemyShip", (40, 0), {}), ("EnemyShip", (80, 0), {})], # At 8 seconds, spawn two enemy ships at (40, 0) and (80, 0)
            12: [("EnemyShip", (40, 0), {}), ("EnemyShip", (80, 0), {}), ("EnemyShip", (120, 0), {})],
        }


    def update(self, dt):
        self.timer.update()


    def on_timer_tick(self):
        self.ticks += 1
        if self.ticks in self.seq:
            tasks : tuple = self.seq[self.ticks]
            for task in tasks:
                arg1 = task[0]
                match arg1:
                    case "EnemyShip":
                        self.spawn_ship(arg1, task[1], task[2])                
    

    def spawn_ship(self, ship, position, property_dict = {}):
        print("Spawn enemy ship!", property_dict)
        img = assets["ship_sheet"].subsurface(pg.Rect(0, 32 * 3, 32, 32))
        enemy_ship = EnemyShip(img, position, property_dict)
        enemy_ship.on_destroyed = handle_enemy_destroyed





pg.init()
pg.mixer.init()
screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pg.Clock()
load_resources()

starfield = Starfield((SCREENWIDTH, SCREENHEIGHT), 400)
stars = []
sizes = [1, 2, 2, 2, 2, 4, 4, 8]
for _ in range(100):
    star = Star(random.randint(0, SCREENWIDTH), random.randint(0, SCREENHEIGHT), random.choice(sizes))
    stars.append(star)

# wave manager
wavemanager = WaveManager()


# font and text
font = pg.font.SysFont("Verdana", 12)

# score
score = 0
scoresurf = font.render(f"Score: {score}", True, (255, 255, 255))
def handle_enemy_destroyed():
    global score
    score += 100

# ships
ship_image = assets["ship_sheet"].subsurface(pg.Rect(0, 0, 32, 32))
ship = PlayerShip(ship_image, (140, 500))


running = True
while running:
    dt = clock.tick(60) / 1000

    starfield.render(screen)

    for s in stars:
        s.update(dt)
        s.render(screen)

    wavemanager.update(dt)

    ship_group.update(dt)
    bullet_group.update(dt)

    ship_group.draw(screen)
    bullet_group.draw(screen)

    # render score
    scoresurf = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(scoresurf, scoresurf.get_rect(topleft=(10, 10)))

    pg.display.flip()
    events = pg.event.get()
    for e in events:
        if e.type == pg.QUIT:
            running = False

pg.quit()