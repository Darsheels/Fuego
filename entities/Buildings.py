import pygame

class FireStation:
    def __init__(self , x ,y):
        CURRENT_SCALING  = 11
        
        self.image = pygame.image.load("assets/sprites/buildings/Fire Department.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (128 * CURRENT_SCALING,128 * CURRENT_SCALING))
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.door_zone = pygame.Rect(x + 200 , y + 900 , 100 , 100)
        
    def draw(self,surface):
        surface.blit(self.image , self.rect)
        