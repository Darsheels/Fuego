import pygame
from config import SCREEN_WIDTH , SCREEN_HEIGHT , FPS , BG_COLOR , GROUND_LEVEL
from game.entities.StarterVehicle import DefaultVehicle
from game.entities.buildings import FireStation , CommercialBuilding
from game.entities.Button import Button
from game.entities.FireFighter import Firefighter


class Engine:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
        pygame.display.set_caption("Fuego")
        self.clock = pygame.time.Clock()
        self.running = True
        
        
        self.background = pygame.image.load("assets/images/Fuego_BG.png").convert_alpha()
        self.ground = pygame.image.load("assets/images/Ground.png").convert_alpha()
        
        
        self.background = pygame.transform.scale(
            self.background , (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        
        self.ground = pygame.transform.scale(
            self.ground , (100000  , 300)
        )
        
        self.defaultVehicle = DefaultVehicle(100, GROUND_LEVEL) 
        self.fireStation = FireStation(213 , -70)
        self.commercialBuilding = CommercialBuilding(213 , -70)
        self.button = Button(0,0)
        
        self.firefighter = Firefighter(213 , 590)
        self.buildings =  [self.fireStation , self.commercialBuilding]
        self.current_building = 0
        
        
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
                
            if self.button.is_clicked(event):
                self.current_building = (self.current_building + 1) % len(self.buildings)
               
                
    def update(self):
        self.defaultVehicle.update()
        self.firefighter.update()
    
    def draw(self):
        self.screen.blit(self.background , (0,0))
        self.screen.blit(self.ground , (0 , 450))
    
        self.buildings[self.current_building].draw(self.screen)
        self.button.draw(self.screen)
        self.firefighter.draw(self.screen)
       
       
        pygame.display.flip()
