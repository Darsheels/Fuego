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
        self.current_scene = "outside"
        
        self.near_door = False
        
    def enter_building(self):
        print("Entering Building ...")
        self.current_scene = "interior"
        
        
    def draw_interior(self):
        self.screen.fill((20,20,20))
        font = pygame.font.Font(None,60)
        text = font.render("Inside Building" , True , (255 ,255 ,255))
        self.screen.blit(text , (200,200))
        
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
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e and self.near_door:
                    self.enter_building()
            
            if self.button.is_clicked(event):
                self.current_building = (self.current_building + 1) % len(self.buildings)
               
                
    def update(self):
        self.defaultVehicle.update()
        self.firefighter.update()
        
        player_rect = self.firefighter.rect
        current_building = self.buildings[self.current_building]
        
        self.near_door = current_building.door_zone.colliderect(player_rect)
        
        
    def draw(self):
        
        if self.current_scene == "interior":
            self.draw_interior()
            return
        
        
        self.screen.blit(self.background , (0,0))
        self.screen.blit(self.ground , (0 , 450))
    
        building = self.buildings[self.current_building]
        building.draw(self.screen)
        
        
        self.button.draw(self.screen)
        self.firefighter.draw(self.screen)
       
       
       
       
        if self.near_door:
            font = pygame.font.Font(None , 40)
            text =font.render("Press E" , True , (255,255,255))
            self.screen.blit(text , (building.door_zone.x , building.door_zone.y - 30))
       
        pygame.display.flip()
