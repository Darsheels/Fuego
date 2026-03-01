import pygame
from settings import SCREEN_HEIGHT , SCREEN_WIDTH , FPS
from entities.Player import Player
from entities.Buildings import FireStation

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT))
        pygame.display.set_caption("Fuego")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.background = pygame.image.load("assets/images/Background.png").convert_alpha()
        self.background = pygame.transform.scale(
            self.background , (256 * 9 , 256 * 9)
        )
        
        self.ground = pygame.image.load("assets/images/Ground.png").convert_alpha()
        self.ground = pygame.transform.scale(
            self.ground , (SCREEN_WIDTH , 300)
        )
        
        self.player = Player(400 , 480)
        self.interior_player = Player(800 , 570)
        self.fire_Station = FireStation(0 , -375)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player , self.interior_player)
        
        
        self.current_scene = "outside"
        self.near_door = False
        
        
    def enter_building(self):
        print("Entering Building ...")
        self.current_scene = "interior"
        
        
    def draw_interior(self):
        self.fireDep_interior = pygame.image.load("assets/images/buildings/RealinnerFireDepartment.png")
        self.fireDep_interior = pygame.transform.scale(self.fireDep_interior , (256 * 5 , 256 * 5)
        ) 
        self.screen.blit(self.fireDep_interior , (0,0))
        
    
    
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
                
    def update(self):
        keys = pygame.key.get_pressed()
        
        if self.current_scene == "outside":
            self.player.update(keys)
            player_rect = self.player.rect
            self.near_door = self.fire_Station.door_zone.colliderect(player_rect)
        else:
            self.interior_player.update(keys)
        
       
    
    def draw(self):
        keys = pygame.key.get_pressed()
        
        if self.current_scene == "interior":
            self.draw_interior()
            self.interior_player.draw(self.screen)
            pygame.display.flip()
            return
        
        self.screen.blit(self.background , (0,0))
        self.screen.blit(self.ground , (0 , 450))
        
        self.fire_Station.draw(self.screen)
        self.player.draw(self.screen)
        
        
        if self.near_door:
            font = pygame.font.Font(None , 40)
            text = font.render("Press E" , True , (255,255,255))
            self.screen.blit(text, (self.fire_Station.door_zone.x , self.fire_Station.door_zone.y - 30))
        
        pygame.display.flip()