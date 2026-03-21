import pygame

class Pager():
    def __init__(self, x, y):
        self.image = pygame.image.load("assets/sprites/buildingblocks/pager.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect(topleft=(x, y))        


    def update(self, keys):
        pass


    def draw(self, screen):
        screen.blit(self.image, self.rect)