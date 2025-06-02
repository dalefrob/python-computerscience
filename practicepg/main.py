import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Hello PyGame!")

clock = pygame.time.Clock()

surf = pygame.Surface((50, 50))
surf.fill((255,0,0))
rect = pygame.Rect(200,200, 50, 50)

running = True  # What are all the variable types??
while running:
    screen.fill((255,255,255))
    screen.blit(surf, rect)
    pygame.display.flip()

    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
    
    key = pygame.key.get_pressed()
    print(key)
    if key[pygame.K_RIGHT]: 
        rect.x += 1
        print(rect)
    elif key[pygame.K_LEFT]:
        rect.x -= 1
    
    clock.tick(60)