import pygame
from entities.scene_manager import SceneManager
from entities.Player import Player
from entities.Buildings import FireStation , TruckApparatus , LockerRoom , map
from entities.scene_config import SPAWN_POINTS
from entities.vehicles import DefaultTruck
from entities.pager import Pager
from settings import SCREEN_WIDTH


class FireStationOutsideScene:
    def __init__(self , game , player):
        self.game = game
        self.player = player
        self.fire_station = FireStation(0 , -375)
        
        self.interior_spawn = SPAWN_POINTS["fire_station_interior"]["default_interior"]
        
        self.outside_spawn = SPAWN_POINTS["outside"]["default"]
        
        self.player.rect.topleft = self.outside_spawn
        
    def update(self,keys,dt):
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
        
        


            
class FireTruckDrivingScene:
    def __init__(self , game , fire_truck):
        self.game = game
        self.fire_truck = fire_truck
        self.fire_station = FireStation(0 , -375)
       
        
    def update(self , keys , dt):
        self.fire_truck.update(keys)
        if keys[pygame.K_l]:
            self.game.player.rect.topleft = SPAWN_POINTS["outside"]["fire_station_exit"]
            self.game.scene_manager.set("outside")
            self.fire_truck.speed = 0
        if self.fire_truck.rect.right > SCREEN_WIDTH:
            self.game.scene_manager.set("community_map")
            
        
    def draw(self,screen):
        screen.blit(self.game.background , (0,0))
        screen.blit(self.game.ground, (0,450))
        self.fire_station.draw(screen)
        self.fire_truck.draw(screen)
       
       
class CommunityMap:
    def __init__(self , game , truck):
        self.game = game
        self.truck = truck
        self.map = map(0,0)
        
    def update(self , keys , dt):
        self.truck.update(keys)
        
        
    def draw(self , screen):
        self.map.draw(screen)
        self.truck.draw(screen)
        