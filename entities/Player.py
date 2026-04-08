import pygame
from entities.animation import load_sprite_sheet , Animation


class Player(pygame.sprite.Sprite):
    def __init__(self,x,y):
       super().__init__()
       
       self.walk_frames = load_sprite_sheet("assets/sprites/player/DefaultPlayer.png" , 32 , 32 , scale=7)
       self.idle_frames = load_sprite_sheet("assets/sprites/player/idleFireFighter.png" , 32 , 32 , scale=7)
       
       self.walk_anim = Animation(self.walk_frames , speed= 0.1 , breaker=False)
       self.idle_anim = Animation(self.idle_frames , speed=0.1 , breaker=False)
       
       self.image = self.idle_anim.image
       self.rect = self.image.get_rect(topleft=(x,y))
       
       self.in_vehicle = False
       self.visible = True
       
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
        if self.visible:
            surface.blit(self.image , self.rect)  
       
    
class FireFighter(pygame.sprite.Sprite):
    def __init__(self,x,y):
       super().__init__()
       
       self.walk_frames = load_sprite_sheet("assets/sprites/player/Firefighter.png" , 48 , 96 , scale=2)
       self.idle_frames = load_sprite_sheet("assets/sprites/player/IdleGearedFireFighter.png" , 48 , 96 , scale=2)
       
       self.walk_anim = Animation(self.walk_frames , speed= 0.1 , breaker=False)
       self.idle_anim = Animation(self.idle_frames , speed=0.1 , breaker=False)
       
       self.image = self.idle_anim.image
       self.rect = self.image.get_rect(topleft=(x,y))
       
       self.in_vehicle = False
       self.visible = True
       
       self.speed = 2
       self.facing_right = True
       
       self.ladder = None
       self.on_ladder = False
       self.climbing = False
       
    def update(self , keys):
        moving = False
        
        if self.on_ladder:
            self.climbing = False
            moving = False
            self.rect.centerx = self.ladder.zone.centerx
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
                self.climbing = True
               
            if keys[pygame.K_s]:
                self.rect.y += self.speed
                self.climbing = True
            
            if self.rect.top < self.ladder.zone.top:
                self.rect.top = self.ladder.zone.top
                self.on_ladder = False
                self.climbing = False
                if keys[pygame.K_s]:
                    self.on_ladder = True
                    self.climbing = True

            if self.rect.bottom > self.ladder.zone.bottom:
                self.rect.bottom = self.ladder.zone.bottom
                self.on_ladder = False
                self.climbing = False
                if keys[pygame.K_w]:
                    self.on_ladder = True
                    self.climbing = True
                
        else:
            self.climbing = False     
              
        if not self.on_ladder and not self.climbing:
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
        if self.visible:
            surface.blit(self.image , self.rect)