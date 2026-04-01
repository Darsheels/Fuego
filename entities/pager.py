import pygame

class Pager():
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/sprites/buildingblocks/pager.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(topleft=(x, y))        

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
            screen.blit(self.image, self.rect)