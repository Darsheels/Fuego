import pygame
from config import SCREEN_WIDTH , SCREEN_HEIGHT , FPS , BG_COLOR
from game.entities.StarterVehicle import DefaultVehicle

class Engine:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        pygame.display.set_caption("Fuego")
        self.clock = pygame.time.Clock()
        self.running = True
        
        
        self.background = pygame.image.load("assets/images/Fuego_BG.png").convert_alpha()
        self.ground = pygame.image.load("assets/images/Ground.png").convert_alpha()
        
        self.fireDepartment = pygame.image.load("assets/images/buildings/Fire Department.png").convert_alpha()
        
        self.background = pygame.transform.scale(
            self.background , (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        
        self.fireDepartment = pygame.transform.scale(
            self.fireDepartment , (1100 ,750)
        )
        
        self.ground = pygame.transform.scale(
            self.ground , (100000  , 300)
        )
        
        self.defaultVehicle = DefaultVehicle(100, 570) 
        
        
        
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
        self.defaultVehicle.update()
    
    def draw(self):
        self.screen.blit(self.background , (0,0))
        self.screen.blit(self.ground , (0 , 450))
        self.screen.blit(self.fireDepartment , (213 , -70))
        self.defaultVehicle.draw(self.screen)
        
        
        pygame.display.flip()
