import pygame

class DefaultTruck:
    def __init__(self , x ,y):
        CURRENT_SCALING = 8
        
        original= pygame.image.load("assets/sprites/vehicles/FireTruck.png").convert_alpha()
        original = pygame.transform.scale(original , (92 * CURRENT_SCALING , 64 * CURRENT_SCALING))
        
        self.image_right = original
        self.image_left = pygame.transform.flip(original , True , False)
        
        self.image = self.image_right
        
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.truck_zone = pygame.Rect(x + 100 , y + 300 , 100 , 100)
        
        self.speed = 0
        self.max_speed = 8
        self.acceleration = 0.5
        self.friction = 0.85
        
        
    def update(self , keys):
        pass
        
    
        # if keys[pygame.K_a]:
        #     self.speed -= self.acceleration
        #     self.image = self.image_left
            
        
        # if keys[pygame.K_d]:
        #     self.speed += self.acceleration
        #     self.image = self.image_right
            
        # if not (keys[pygame.K_a] or  keys[pygame.K_d]):
        #     self.speed *= self.friction
            
        # self.speed = max(-self.max_speed, min(self.speed , self.max_speed))
        
        # self.rect.x += self.speed
        
       
        
    def draw(self,surface):
        surface.blit(self.image, self.rect)
        