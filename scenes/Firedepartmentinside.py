import pygame
from entities.scene_manager import SceneManager
from entities.Player import Player
from entities.Buildings import FireStation , TruckApparatus , LockerRoom , House1
from entities.scene_config import SPAWN_POINTS
from entities.vehicles import DefaultTruck
from entities.pager import Pager
from settings import SCREEN_WIDTH , SCREEN_HEIGHT
from entities.UI_prompt import UIPrompt
        
class FireStationInteriorScene:
    def __init__(self , game , player):
        self.game = game
        self.player = player
        self.TruckApparitus = TruckApparatus(0 , -100)
       
        self.display_truck = DefaultTruck(50,300)
       
        self.interior_spawn = SPAWN_POINTS["fire_station_interior"]["default_interior"]
        
        self.outside_spawn = SPAWN_POINTS["outside"]["fire_station_exit"]
        
        self.locker_room_entry = SPAWN_POINTS["locker_room"]["default"]
        
        self.player.rect.topleft = self.interior_spawn 
        
        self.exit_firedept = UIPrompt("Press E to exit", 800 , 480)
        self.enter_fire_truck_prompt = UIPrompt("Press X to enter the fire truck", 300 , 600)
        
        self.pager = Pager(1000,500)
        
    def enter_fire_truck(self):
        self.time_inside = 0
        self.pager_triggered = False
        
        self.player.in_vehicle = True
        
        self.player.visible = False
        
        spawn = SPAWN_POINTS["outside"]["fire_truck_spawn"]
        self.game.fire_truck.rect.topleft = spawn
        
        self.game.scene_manager.set("driving")
        
        
    def update(self, keys , dt):
        self.player.update(keys)
        
        self.pager.update(dt)
        
           
        if self.TruckApparitus.door_zone.colliderect(self.player.rect):
            self.exit_firedept.show()
            
            if keys[pygame.K_e]:
                self.player.rect.topleft = self.outside_spawn
                self.game.scene_manager.set("outside")
        else:
            self.exit_firedept.hide()
     
        if self.display_truck.truck_zone.colliderect(self.player.rect):
            self.enter_fire_truck_prompt.show()
            
            if keys[pygame.K_x]:
                self.enter_fire_truck()
        else:
            self.enter_fire_truck_prompt.hide()

        if self.player.rect.right >= SCREEN_WIDTH:
            self.player.rect.topleft = self.locker_room_entry
            self.game.scene_manager.set("locker_room")


            
    def draw(self , screen):
        self.TruckApparitus.draw(screen)
        self.player.draw(screen)
        self.display_truck.draw(screen)
        self.pager.draw(screen)
        self.exit_firedept.draw(screen)
        self.enter_fire_truck_prompt.draw(screen)

            
     
            
class LockerRoomScene:
    def __init__(self,game,player):
        self.game = game
        self.player = player
        self.locker_room = LockerRoom(0 , -200)
        self.pager = Pager(1000,500)
        
        self.interior_spawn = SPAWN_POINTS["locker_room"]["default"]
        
        self.player.rect.topleft = self.interior_spawn
        
    def update(self,keys,dt):
        self.player.update(keys)
        self.pager.update(dt)
        
        if self.player.rect.left < 0:
            self.player.rect.topleft = SPAWN_POINTS["fire_station_interior"]["left_entry"]
            self.game.scene_manager.set("fire_station_interior")
        
    def draw(self,screen):
        self.locker_room.draw(screen)
        self.pager.draw(screen)
        self.player.draw(screen)

