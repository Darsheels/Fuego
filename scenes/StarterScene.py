# import pygame
# from entities.Scenes import BaseScene
# from entities.Buildings import FireStation , TruckApparatus , LockerRoom , House1
# from entities.scene_config import SPAWN_POINTS
# from entities.vehicles import DefaultTruck
# from settings import SCREEN_WIDTH ,SCREEN_HEIGHT

# class FireStationOutsideScene(BaseScene):
#     def __init__(self , game , player):
#         super().__init__(game, player)
#         self.fire_station = FireStation(0 , -375)
#         self.add_objects(self.fire_station)
#         self.add_interaction(
#             "enter_fire_station",
#             "Press E to enter the fire station",
#             zone=self.fire_station.door_zone,
#             key=pygame.K_e,
#             target_scene="fire_station_interior",
#             spawn_point="default_interior")

#     def on_enter(self):
#         spawn_name = self.game.next_spawn if self.game.next_spawn is not None else "default"
#         self.player.rect.topleft = SPAWN_POINTS["outside"][spawn_name]
#         self.game.next_spawn = None
        
#     def draw(self,screen):
#         screen.blit(self.game.background, (0,0))
#         screen.blit(self.game.ground, (0,450))
#         super().draw(screen)


# class FireTruckDrivingScene(BaseScene):
#     def __init__(self , game , player ,  fire_truck):
#         super().__init__(game, player)
#         self.fire_truck = fire_truck
#         self.fire_station = FireStation(0 , -375)
#         self.add_objects(self.fire_station)
#         self.add_objects(self.fire_truck)
#         self.add_transition("House1", direction="right", spawn_point="left_entry")

        
#     def on_enter(self):
#         if self.player:
#             self.player.in_vehicle = True
#             self.player.visible = False
            
#         spawn_name = self.game.next_spawn if self.game.next_spawn is not None else "default"
#         self.player.rect.topleft = SPAWN_POINTS["outside"][spawn_name]
#         self.game.next_spawn = None

#     def exit_fire_truck(self):
#         self.player.in_vehicle = False
#         self.player.visible = True
        
#         exit_x = self.game.fire_truck.rect.x 
#         exit_y = self.game.fire_truck.rect.y 
#         self.player.rect.topleft = (exit_x, exit_y)
        
#         self.game.scene_manager.set("outside")
        
#     def update(self , keys , dt):
#         super().update(keys, dt)

#         if self.player and keys[pygame.K_l] and self.player.in_vehicle:
#             self.exit_fire_truck()
            
#     def draw(self,screen):
#         screen.blit(self.game.background , (0,0))
#         screen.blit(self.game.ground, (0,450))
#         super().draw(screen)
       
       
       
       
# class House1Scene(BaseScene):
#     def __init__(self , game , truck):
#         super().__init__(game, None)
#         self.fire_truck = truck
#         self.house = House1(0,-350)
#         self.add_objects(self.house)
#         self.add_objects(self.fire_truck)
#         self.add_transition("driving", direction="left", spawn_point="right_entry")
        
#     def on_enter(self):
#         spawn_name = self.game.next_spawn if self.game.next_spawn is not None else "default"
#         self.fire_truck.rect.x = SPAWN_POINTS["house1"][spawn_name][0]
#         self.fire_truck.rect.bottom = 780
#         self.game.next_spawn = None
        
#     def update(self , keys , dt):
#         super().update(keys, dt) 

#     def draw(self , screen):
#         screen.blit(self.game.background , (0,0))
#         screen.blit(self.game.ground, (0,450))
#         super().draw(screen)
        