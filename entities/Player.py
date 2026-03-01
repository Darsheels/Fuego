import pygame
from entities.animation import load_sprite_sheet , Animation


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
       super().__init__()
       
       self.walk_frames = load_sprite_sheet("assets/sprites/player/DefaultPlayer.png" , 32 , 32)
       self.idle_frames = load_sprite_sheet("assets/sprites/player/idleFireFighter.png" , 32 , 32)
       
       self.walk_anim = Animation(self.walk_frames , speed= 0.1)
       self.idle_anim = Animation(self.idle_frames , speed=0.1)
       
       self.image = self.idle_anim.image
       self.rect = self.image.get_rect(topleft=(x,y))
       
       self.speed = 2
       self.facing_right = True
       
    def update(self , keys):
        moving = False
        
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            moving = True
            self.facing_right = False
        
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            moving = True
            self.facing_right = True
            
        if moving:
           self.walk_anim.update()
           frame = self.walk_anim.image
        else:
           self.idle_anim.update()
           frame = self.idle_anim.image
            
        if self.facing_right:
            self.image = frame
        else:
            self.image = pygame.transform.flip(frame , True , False)
            
    
    def draw(self , surface):
        surface.blit(self.image , self.rect)  
       
    