import pygame

class Player:
    def __init__(self , x , y):
        self.original_image = pygame.image.load("assets/images/player/NewFireFighter.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image , (32 * 5 , 32 * 5))
        
        self.image = self.original_image
        self.rect  = self.image.get_rect(center=(x,y))
        self.speed = 2
        
        frames = [
            pygame.image.load("assets/images/player/NewFireFighter.png").convert_alpha(),
            pygame.image.load("assets/images/player/NewFireFighter2.png").convert_alpha(),
            pygame.image.load("assets/images/player/NewFireFighter3Real.png").convert_alpha(),
            pygame.image.load("assets/images/player/FireFighter3Real.png").convert_alpha(),
            pygame.image.load("assets/images/player/NewFireFighter3.png").convert_alpha()
        ]
        
        self.walkRight_frames = [pygame.transform.scale(f,(32 * 7 , 32 * 7)) for f in frames]
        self.walkLeft_frames = [pygame.transform.flip(f , True , False) for f in self.walkRight_frames]
        
        self.frame_index = 0
        self.frame_speed = 0.10
        
        self.facing_right = True
        
        self.image = self.walkRight_frames[0]
        
        
    def update(self):
        moving = False
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            moving = True
            self.facing_right = False
            self.rect.x -= self.speed
            
        if keys[pygame.K_d]:
            moving = True
            self.facing_right = True
            self.rect.x += self.speed
            
        if moving:
            self.frame_index += self.frame_speed
            if self.frame_index >= len(self.walkLeft_frames):
                self.frame_index = 0
            if self.facing_right:
                self.image = self.walkRight_frames[int(self.frame_index)]
            else:
                self.image = self.walkLeft_frames[int(self.frame_index)]
        else:
            self.image = self.walkRight_frames[0] if self.facing_right else self.walkLeft_frames[0]
            
    
    def draw(self,surface):
        surface.blit(self.image, self.rect)