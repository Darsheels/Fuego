import pygame

class FireStation:
    def __init__(self , x ,y):
        CURRENT_SCALING  = 11
        
        self.image = pygame.image.load("assets/sprites/buildings/Fire Department.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (128 * CURRENT_SCALING,128 * CURRENT_SCALING))
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.door_zone = pygame.Rect(x + 150 , y + 900 , 100 , 100)
        
    def draw(self,surface):
        surface.blit(self.image , self.rect)
        
        
class TruckApparatus:
    def __init__(self,x,y):
        CURRENT_SCALING = 5
        
        self.image = pygame.image.load("assets/sprites/buildings/RealInnerFireDepartment.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (256 * CURRENT_SCALING , 256 * CURRENT_SCALING))
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.door_zone = pygame.Rect(x + 1000 , y + 500 , 100 , 100)
        
    def draw(self,surface):
        surface.blit(self.image , self.rect)
        
        
class LockerRoom:
    def __init__(self,x,y):
        CURRENT_SCALING = 5
        
        self.image = pygame.image.load("assets/sprites/buildings/LockerRoom.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (256 * CURRENT_SCALING , 256 * CURRENT_SCALING))
        self.rect = self.image.get_rect(topleft=(x,y))
        
    def draw(self,surface):
        surface.blit(self.image , self.rect)
        
        
        
class map:
    def __init__(self,x,y):
        CURRENT_SCALING = 5
        
        self.image = pygame.image.load("assets/sprites/buildings/tempmap.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (256 * CURRENT_SCALING , 256 * CURRENT_SCALING))
        self.rect = self.image.get_rect(topleft=(x,y))
        
    def draw(self,surface):
        surface.blit(self.image , self.rect)