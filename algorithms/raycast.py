import pygame
import sys
import math

#global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)

FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 120
MAX_DEPTH = 500
STEP_ANGLE = FOV / CASTED_RAYS

# 3d projection
SCALE = (SCREEN_WIDTH / 2) / CASTED_RAYS

# Encapsulate values into an object to avoid global scope errors in functions
player = {
    'x': (SCREEN_WIDTH / 2) / 2,
    'y': (SCREEN_WIDTH / 2) / 2,
    'angle': math.pi
}

MAP = ('########'
       '# #    #'    
       '# #  ###'    
       '#      #'   
       '##     #'   
       '#  ### #'   
       '#   #  #'  
       '########')

def draw_map():    
    #colors
    light_grey = (191, 191, 191)
    dark_grey = (65, 65, 65)
    
    #iterate over map    
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):            
            #calculate square index            
            square = i * MAP_SIZE + j
            
            #draw map            
            pygame.draw.rect(win, 
                light_grey if MAP[square] == '#' else dark_grey,                
                (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1))
    #draw player    
    pygame.draw.circle(win, (162, 0, 255), (int(player["x"]), int(player["y"])), 12)


#draw rays
def draw_rays():
    start_angle = player["angle"] - HALF_FOV    
    
    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            # get ray target coords
            target_x = player["x"] - math.sin(start_angle) * depth
            target_y = player["y"] + math.cos(start_angle) * depth

            #convert target x, y coordinates to map col, row
            col = int(target_x / TILE_SIZE)           
            row = int(target_y / TILE_SIZE)  
            
            #calculate map square index            
            square = row * MAP_SIZE + col

            #wall shading                
            color = 255 / (1 + depth * depth * 0.0001)

            #calculate wall height
            wall_height = 21000 / (depth + 0.0001)

            if MAP[square] == '#':
                # Highligh the tile hit                
                pygame.draw.rect(win, (195, 137, 38), 
                                (col * TILE_SIZE, row * TILE_SIZE, 
                                TILE_SIZE - 1, TILE_SIZE - 1))                                
                # Draw the ray line in 2d
                pygame.draw.line(win, (233, 166, 49), (player["x"], player["y"]), (target_x, target_y))    
                
                #Draw 3D projection
                pygame.draw.rect(win, (color, color, color),
                                (SCREEN_HEIGHT + ray * SCALE,
                                (SCREEN_HEIGHT / 2) - wall_height / 2, SCALE, wall_height))                            
                
                break # This stops the loop checking the rest of depth!
    
        start_angle += STEP_ANGLE


def player_input():
    #get user input    
    keys = pygame.key.get_pressed()

    #handle user input    
    if keys[pygame.K_LEFT]:        
        #working with radians, not degrees       
        player["angle"] -= 0.1
    elif keys[pygame.K_RIGHT]:        
        player["angle"] += 0.1    
    elif keys[pygame.K_UP]:        
        player["x"] += -1 * math.sin(player["angle"]) * 5        
        player["y"] += math.cos(player["angle"]) * 5    
    elif keys[pygame.K_DOWN]:        
        player["x"] -= -1 * math.sin(player["angle"]) * 5        
        player["y"] -= math.cos(player["angle"]) * 5


#game window
pygame.init()
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ray-casting')
clock = pygame.time.Clock()

#game loop
while True:    
    for event in pygame.event.get():        
        if event.type == pygame.QUIT:            
            pygame.quit()
            sys.exit(0)
    
    # update 2D map background    
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))
    # update 3D background    
    pygame.draw.rect(win, (100, 100, 100), (480, SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))    
    pygame.draw.rect(win, (200, 200, 200), (480, -SCREEN_HEIGHT / 2, SCREEN_HEIGHT, SCREEN_HEIGHT))

    player_input()
    draw_map()
    draw_rays()
    
    #update display    
    pygame.display.flip()
    
    #set FPS    
    clock.tick(30)

