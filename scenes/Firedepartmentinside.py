# import pygame
# from entities.Scenes import BaseScene
# from entities.Player import Player
# from entities.Buildings import FireStation , TruckApparatus , LockerRoom , House1
# from entities.scene_config import SPAWN_POINTS
# from entities.vehicles import DefaultTruck
# from settings import SCREEN_WIDTH , SCREEN_HEIGHT

# class FireStationInteriorScene(BaseScene):
#     def __init__(self, game, player):
#         super().__init__(game, player)
#         self.TruckApparatus = TruckApparatus(0, -100)
#         self.display_truck = DefaultTruck(50, 300)
#         self.add_objects(self.TruckApparatus)
#         self.add_objects(self.display_truck)
#         self.add_interaction("exit", "Press E to exit", zone=self.TruckApparatus.door_zone, key=pygame.K_e, target_scene="outside", spawn_point="default")
#         self.add_interaction("enter_truck", "Press X to enter the fire truck", zone=self.display_truck.truck_zone, key=pygame.K_x, target_scene="truck_cutscene", spawn_point="default")
#         self.add_transition("locker_room", direction="right", spawn_point="locker_room_entry")
#         self.add_pager()

#     def on_enter(self):
#         spawn_name = self.game.next_spawn if self.game.next_spawn is not None else "default_interior"
#         self.player.rect.topleft = SPAWN_POINTS["fire_station_interior"][spawn_name]
#         self.game.next_spawn = None


# class LockerRoomScene(BaseScene):
#     def __init__(self, game, player):
#         super().__init__(game, player) 
#         self.locker_room = LockerRoom(0, -200)
#         self.add_objects(self.locker_room)
#         self.add_transition("fire_station_interior", direction="left", spawn_point="left_entry")
#         self.add_pager()

#     def on_enter(self):
#         spawn_name = self.game.next_spawn if self.game.next_spawn is not None else "default"
#         self.player.rect.topleft = SPAWN_POINTS["locker_room"][spawn_name]
#         self.game.next_spawn = None







