import pygame
from .Scaler import Entity

class DefaultTruck(Entity):
    def __init__(self, x, y):
        super().__init__("assets/sprites/vehicles/FireTruck.png", (92, 64), x, y)
        self.image_right = self.image
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right

    def update(self, keys):
        pass

        