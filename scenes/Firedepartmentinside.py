import pygame
from entities.scene_manager import SceneManager
from entities.Player import Player
from entities.Buildings import FireStation , TruckApparatus , LockerRoom , House1
from entities.scene_config import SPAWN_POINTS
from entities.vehicles import DefaultTruck
from entities.pager import Pager
from settings import SCREEN_WIDTH , SCREEN_HEIGHT
from entities.UI_prompt import UIPrompt
from entities.Scenes import BaseScene
        

class FireStationInteriorScene(BaseScene):
    def __init__(self, game, player):
        super().__init__(game, player)

        spawn_name = self.game.next_spawn if self.game.next_spawn is not None else "default_interior"
        self.player.rect.topleft = SPAWN_POINTS["fire_station_interior"][spawn_name]
        self.TruckApparatus = TruckApparatus(0, -100)
        
        self.display_truck = DefaultTruck(50, 300)
        self.add_objects(self.TruckApparatus)
        self.add_objects(self.display_truck)

        self.add_interaction("exit", "Press E to exit", zone=self.TruckApparatus.door_zone, key=pygame.K_e, target_scene="outside", spawn_point= "default")
        self.add_interaction("enter_truck", "Press X to enter the fire truck", zone= self.display_truck.truck_zone, key=pygame.K_x, target_scene="driving", spawn_point="default")
        
        self.add_transition("locker_room", direction="right" , spawn_point= "locker_room_entry")
        self.add_pager()

            
     
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

