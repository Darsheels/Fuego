import pygame
from entities.scene_manager import SceneManager
from entities.Player import Player
from entities.Buildings import FireStation
from entities.scene_config import SPAWN_POINTS

class FireStationOutsideScene:
    def __init__(self , game , player):
        self.game = game
        self.player = player
        self.fire_station = FireStation(0 , -375)
        
        self.interior_spawn = SPAWN_POINTS["fire_station_interior"]["default"]
        
        self.outside_spawn = SPAWN_POINTS["outside"]["fire_station_exit"]
        
        self.player.rect.topleft = self.outside_spawn
        
    def update(self,keys):
        self.player.update(keys)
        
        if self.fire_station.door_zone.colliderect(self.player.rect):
            if keys[pygame.K_e]:
                self.player.rect.topleft = self.interior_spawn
                self.game.scene_manager.set("fire_station_interior")
                
    def draw(self,screen):
        screen.blit(self.game.background, (0,0))
        screen.blit(self.game.ground, (0,450))
        self.fire_station.draw(screen)
        self.player.draw(screen)
        
        
        
        
class FireStationInteriorScene:
    def __init__(self , game , player):
        self.game = game
        self.player = player
        self.background = pygame.image.load("assets/sprites/buildings/RealInnerFireDepartment.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (256 * 5 , 256 * 5))
       
       
        self.interior_spawn = SPAWN_POINTS["fire_station_interior"]["default"]
        self.outside_spawn = SPAWN_POINTS["outside"]["fire_station_exit"]
        
        self.player.rect.topleft = self.outside_spawn
    def update(self,keys):
        self.player.update(keys)
        
        if keys[pygame.K_e] and self.player.rect.x < 100:
            self.player.rect.topleft = self.outside_spawn
            self.game.scene_manager.set("outside")
            
    def draw(self , screen):
        screen.blit(self.background , (0,0))
        self.player.draw(screen)
            