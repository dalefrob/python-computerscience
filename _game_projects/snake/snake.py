import pygame

PARTSIZE = 10
OFFSET = 10

snake_list = []
snake_length = 5

x = 200
y = 200

move_offset = [0,0]

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

running = True
while running:
    # fill the screen
    screen.fill((45, 75, 110))

    # event handling
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
    

    # controls
    pressed_key = pygame.key.get_just_pressed()
    if pressed_key[pygame.K_UP]:
        move_offset = [0, -1]
    if pressed_key[pygame.K_DOWN]:
        move_offset = [0, 1]
    if pressed_key[pygame.K_LEFT]:
        move_offset = [-1, 0]
    if pressed_key[pygame.K_RIGHT]:
        move_offset = [1, 0]

    # set the head position
    x += move_offset[0] * PARTSIZE
    y += move_offset[1] * PARTSIZE

    snake_head = [x, y]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        snake_list.pop(0)

    # draw the snake
    for part in snake_list:
        rect = pygame.Rect(part, (PARTSIZE, PARTSIZE))
        pygame.draw.rect(screen, (200,255,0), rect)
    
    # flip the buffer
    pygame.display.flip()
    
    clock.tick(15)

