import pygame

class FireStation:
    def __init__(self , x , y):
        self.image = pygame.image.load("assets/images/buildings/Fire Department.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (1100 ,750))
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.door_zone = pygame.Rect(x + 80 , y + 650 , 100 , 100)
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
        
        
class CommercialBuilding:
    def __init__(self,x,y):
        self.image = pygame.image.load("assets/images/buildings/CommercialBuilding.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (1100 , 730))
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.door_zone = pygame.Rect(x+500 , y + 570 , 60 , 40)
    def draw(self,surface):
        surface.blit(self.image , self.rect)