import pygame
from entities.entity import Entity

class Object(Entity):
    class FireHydrant(Entity):
        def __init__(self, x , y):
            super().__init__("assets/sprites/buildingblocks/FireHydrant.png", (128 , 160),x,y, scale=1)
            
    class Pager(Entity):
        def __init__(self, x, y):
            super().__init__("assets/sprites/buildingblocks/pager.png", (200, 200), x, y, scale=1)
            self.time_inside = 5
            self.pager_triggered = False

        def start_cooldown(self):
            self.time_inside = 5
            self.pager_triggered = False
            print("Pager cooldown started. Time inside reset to 60 seconds.")

        def update(self, dt):
            if not self.pager_triggered:
                self.time_inside -= dt
                if self.time_inside <= 0:
                    self.trigger()
        def trigger(self):
            self.pager_triggered = True

        def draw(self, screen):
            if self.pager_triggered:
                super().draw(screen)

    class DefaultTruck(Entity):
        def __init__(self, x, y):
            super().__init__("assets/sprites/vehicles/FireTruck.png", (92, 64), x, y)
            self.image_right = self.image
            self.image_left = pygame.transform.flip(self.image_right, True, False)
            self.image = self.image_right

        def update(self, keys):
            pass
        
    class Ladder(Entity):
        def __init__(self, x, y, height):
            super().__init__("assets/sprites/buildingblocks/Ladder.png", (64 , height), x, y, scale=5)
            self.zone = self.rect.copy()


    class Car1(Entity):
        def __init__(self, x, y):
            super().__init__("assets/sprites/vehicles/Car1.png", (160, 96), x, y, scale=3)
            
            
    class HealthBar():
        def __init__(self, player,x, y, width=100, height=10):
            self.player = player
            self.rect = pygame.Rect(x, y, width, height)
        
        def update(self):
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y - 20
        
        def draw(self, surface):
            ratio = self.player.health / 100
    
            pygame.draw.rect(surface, (255,0,0), self.rect)
            pygame.draw.rect(surface, (0,255,0), (self.rect.x, self.rect.y, self.rect.width * ratio, self.rect.height))

            