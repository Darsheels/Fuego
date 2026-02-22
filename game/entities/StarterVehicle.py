import pygame
import math

class DefaultVehicle:
    def __init__(self , x , y):
        self.original_image = pygame.image.load("assets/images/vehicles/StarterTruck.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image , (300,250))
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x,y))
        
        self.speed = 0
        self.x = x
        self.y = y
        self.angle = 0
        self.acceleration  = 0.2
        self.max_speed = 6 
        self.friction = 0.05
        
    def update(self):
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.rect.x -= 5
        if keys[pygame.K_d]:
            self.rect.x += 5
            
    
    def draw(self,surface):
        surface.blit(self.image , self.rect)