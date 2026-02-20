import pygame
from config import SCREEN_WIDTH , SCREEN_HEIGHT , FPS , BG_COLOR


class Engine:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        pygame.display.set_caption("Fuego")
        self.clock = pygame.time.Clock()
        self.running = True
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
    def update(self):
        pass
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        pygame.display.flip()
