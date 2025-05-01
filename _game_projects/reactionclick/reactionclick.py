# Project to test the reaction speed of a click
# Great to teach input event and a simple state machine

import sys
import pygame
from pygame.locals import *
import random
import time

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reaction Click Game")


clock = pygame.time.Clock()
FPS = 60

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 72)

# Function to display text on the screen
def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_pixels(CYAN):
    pa_surf = pygame.Surface((19,19))
    pa = pygame.PixelArray(pa_surf)

    # [x][ ][x][ ]
    # [ ][x][ ][x]
    # [x][ ][x][ ]
    # [ ][x][ ][ ]

    arr_w = len(pa)
    arr_h = len(pa[0])
    flip = False
    for i in range(arr_h * arr_w):
        x = i // arr_w
        y = i % arr_h
        if flip:
            pa[x][y] = CYAN
        flip = not flip

    del pa
    return pa_surf

class States:
    WAIT = 0
    TRIGGERED = 1
    CLICKED = 2

state = States.WAIT

wait_time = random.randrange(5,15)
reaction_time = 99999.0

def handle_mouse_click(dict):
    global reaction_time, state
    if state == States.TRIGGERED:
        reaction_time = 0 - wait_time
        state = States.CLICKED


running = True
while(running):

    dt = min(clock.tick(FPS) / 1000.0, 0.05)
    wait_time -= dt

    if wait_time <= 0 and state == States.WAIT:
        state = States.TRIGGERED

    match state:
        case States.WAIT:
            screen.fill(WHITE)
            display_text("Wait for it...", font, GREEN, WIDTH / 2, HEIGHT / 2)
        case States.TRIGGERED:
            screen.fill(RED)
            display_text("Click Now!", font, WHITE, WIDTH / 2, HEIGHT / 2)
        case States.CLICKED:
            screen.fill(WHITE)
            display_text(str(reaction_time), font, BLACK, WIDTH / 2, HEIGHT / 2)
            
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        print(event)
        if event.type == QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            handle_mouse_click(event.dict)
    