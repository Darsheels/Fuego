import pygame

pygame.init()

SIZE = HEIGHT , WIDTH = 1280 , 720
screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            
    screen.fill("grey")
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()