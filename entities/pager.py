import pygame
from .Scaler import Entity

class Pager(Entity):
    def __init__(self, x, y):
        super().__init__("assets/sprites/buildingblocks/pager.png", (200, 200), x, y, scale=1)
        self.time_inside = 0
        self.pager_triggered = False

    def update(self, dt):
        if not self.pager_triggered:
            self.time_inside += dt
            if self.time_inside >= 5:
                self.trigger()

    def trigger(self):
        self.pager_triggered = True

    def draw(self, screen):
        if self.pager_triggered:
            super().draw(screen)
