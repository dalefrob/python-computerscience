import pygame as pg
import random

SCREENWIDTH = 280
SCREENHEIGHT = 540

class Star():
    def __init__(self, x, y, speed = 10):
        self.position = pg.Vector2(x, y)
        self.surface = pg.Surface((2,2))
        self.surface.fill((255, 255, 255))
        self.speed = speed
    
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

stars = []
for _ in range(100):
    star = Star(random.randint(0, SCREENWIDTH), random.randint(0, SCREENHEIGHT))
    stars.append(star)


running = True
while running:
    dt = clock.tick(60) / 1000

    screen.fill((0, 0, 0))

    for s in stars:
        s.update(dt)
        s.render(screen)

    pg.display.flip()
    events = pg.event.get()
    for e in events:
        if e.type == pg.QUIT:
            running = False

pg.quit()