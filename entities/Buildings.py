import pygame
from entities.entity import Entity


class Building(Entity):
    class FireStation(Entity):
        def __init__(self, x, y):
            super().__init__("assets/sprites/buildings/Fire Department.png", (128, 128), x, y, scale=11)

    class TruckApparatus(Entity):
        def __init__(self, x, y):
            super().__init__("assets/sprites/buildings/RealInnerFireDepartment.png", (256, 256), x, y, scale=5)

    class LockerRoom(Entity):
        def __init__(self, x, y):
            super().__init__("assets/sprites/buildings/LockerRoom.png", (256, 256), x, y, scale=5)

    class House1(Entity):
        def __init__(self, x, y):
            super().__init__("assets/sprites/buildings/house1.png", (256, 256), x, y, scale=5)
            
    class House1Int(Entity):
        def __init__(self, x , y):
            super().__init__("assets/sprites/buildings/House1Int.png", (256 , 256), x, y, scale = 5)
    
    class Museum(Entity):
        def __init__(self,x,y):
            super().__init__("assets/sprites/buildings/Museum.png", (256,256), x ,y, scale=5)