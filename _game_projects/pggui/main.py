import pygame
import pygame_gui

SCREENWIDTH = 800
SCREENHEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

manager = pygame_gui.UIManager((SCREENWIDTH, SCREENHEIGHT))

running = True
while running:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False
            pygame.quit()
    
    pygame.display.update()