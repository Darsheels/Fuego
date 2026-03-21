import pygame
from entities.scene_manager import SceneManager
from entities.Player import Player
from entities.Buildings import FireStation , FireStationInterior
from entities.scene_config import SPAWN_POINTS
from entities.vehicles import DefaultTruck
from entities.pager import Pager


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
        
        
        
class FireStationInteriorScene:
    def __init__(self , game , player):
        self.game = game
        self.player = player
        self.TruckApparitus = FireStationInterior(0 , -100)
       
        self.time_inside = 0
        self.pager_triggered = False
       
        self.display_truck = DefaultTruck(50,300)
       
        self.interior_spawn = SPAWN_POINTS["fire_station_interior"]["default_interior"]
        
        self.outside_spawn = SPAWN_POINTS["outside"]["fire_station_exit"]
        
        self.player.rect.topleft = self.interior_spawn 
        
        self.pager = Pager(1000,600)
        
    def enter_fire_truck(self):
        self.time_inside = 0
        self.pager_triggered = False
        
        spawn = SPAWN_POINTS["outside"]["fire_truck_spawn"]
        self.game.fire_truck.rect.topleft = spawn
        self.game.scene_manager.set("driving")
        
        
    def update(self, keys , dt):
        self.player.update(keys)

        if not self.pager_triggered:
            self.time_inside += dt
            
            if self.time_inside >= 60:
                self.trigger_pager() 
                
        self.pager.update(None)
           
        if self.TruckApparitus.door_zone.colliderect(self.player.rect):
            if keys[pygame.K_e]:
                self.player.rect.topleft = self.outside_spawn
                self.game.scene_manager.set("outside")
     
        if self.display_truck.truck_zone.colliderect(self.player.rect):
            if keys[pygame.K_x]:
                self.enter_fire_truck()
    
    def trigger_pager(self):
        self.pager_triggered = True
        
            
    def draw(self , screen):
        self.TruckApparitus.draw(screen)
        self.player.draw(screen)
        self.display_truck.draw(screen)
        
        if self.pager_triggered:
            self.pager.draw(screen)
     
            
            
            
class FireTruckDrivingScene:
    def __init__(self , game , fire_truck):
        self.game = game
        self.fire_truck = fire_truck
        self.fire_station = FireStation(0 , -375)
        self.fence = pygame.image.load
        
    def update(self , keys , dt):
        self.fire_truck.update(keys)
        if keys[pygame.K_l]:
            self.game.player.rect.topleft = SPAWN_POINTS["outside"]["fire_station_exit"]
            self.game.scene_manager.set("outside")
            self.fire_truck.speed = 0
        
        
    def draw(self,screen):
        screen.blit(self.game.background , (0,0))
        screen.blit(self.game.ground, (0,450))
        self.fire_station.draw(screen)
        self.fire_truck.draw(screen)
       