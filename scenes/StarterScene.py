import pygame
from entities.scene_manager import SceneManager
from entities.Player import Player
from entities.Buildings import FireStation , FireStationInterior
from entities.scene_config import SPAWN_POINTS
from entities.vehicles import DefaultTruck
from entities.loadingMaps import importMap


class FireStationOutsideScene:
    def __init__(self , game , player):
        self.game = game
        self.player = player
        self.fire_station = FireStation(0 , -375)
        
        self.interior_spawn = SPAWN_POINTS["fire_station_interior"]["default_interior"]
        
        self.outside_spawn = SPAWN_POINTS["outside"]["default"]
        
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
        
        self.map = importMap(
            "assets/tiles/InteriorTileSet.png",
            "assets/maps/FireDepartmentIndoor.tmj"
        )
        
        self.game = game
        self.player = player
       
        self.station_interior = FireStationInterior(0,0)
        self.display_truck = DefaultTruck(50,300)
       
        self.interior_spawn = SPAWN_POINTS["fire_station_interior"]["default_interior"]
        
        self.outside_spawn = SPAWN_POINTS["outside"]["fire_station_exit"]
        
        self.player.rect.topleft = self.interior_spawn 
        
    def enter_fire_truck(self):
        spawn = SPAWN_POINTS["outside"]["fire_truck_spawn"]
        self.game.fire_truck.rect.topleft = spawn
        self.game.scene_manager.set("driving")
        
        
    def update(self,keys):
        self.player.update(keys)
        if self.station_interior.door_zone.colliderect(self.player.rect):
            if keys[pygame.K_e]:
                self.player.rect.topleft = self.outside_spawn
                self.game.scene_manager.set("outside")
        if self.display_truck.truck_zone.colliderect(self.player.rect):
            if keys[pygame.K_x]:
                self.enter_fire_truck()
            
            
    def draw(self , screen):
        self.station_interior.draw(screen)
        self.player.draw(screen)
        self.display_truck.draw(screen)
            
            
            
class FireTruckDrivingScene:
    def __init__(self , game , fire_truck):
        self.game = game
        self.fire_truck = fire_truck
        self.fire_station = FireStation(0 , -375)
        
    def update(self , keys):
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
       