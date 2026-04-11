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
       
    
class FireFighter(pygame.sprite.Sprite):
    def __init__(self,x,y):
       super().__init__()
       
       self.walk_frames = load_sprite_sheet("assets/sprites/player/Firefighter.png" , 48 , 96 , scale=2)
       self.idle_frames = load_sprite_sheet("assets/sprites/player/IdleGearedFireFighter.png" , 48 , 96 , scale=2)
       
       self.walk_anim = Animation(self.walk_frames , speed= 0.1 , breaker=False)
       self.idle_anim = Animation(self.idle_frames , speed=0.1 , breaker=False)
       
       self.image = self.idle_anim.image
       self.rect = self.image.get_rect(topleft=(x,y))
       
       self.speed = 2
       self.facing_right = True
       
       self.ladder = None
       self.on_ladder = False
       self.climbing = False
       
       self.show_ladder_prompt = False
       
       self.has_extinguisher = True
       self.extinguisher_active = False
       self.extinguisher_rect = None
       self.extinguisher_appear = False
       
    def update(self , keys):
        moving = False
        
        #Ladder Movement
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
        #Top Exit    
            if self.rect.top < self.ladder.zone.top:
                self.rect.top = self.ladder.zone.top
                self.on_ladder = False
                self.climbing = False
                if keys[pygame.K_s]:
                    self.on_ladder = True
                    self.climbing = True
        #Bottom Exit
            if self.rect.bottom > self.ladder.zone.bottom:
                self.rect.bottom = self.ladder.zone.bottom
                self.on_ladder = False
                self.climbing = False
        else:
            self.climbing = False     
        
        #Normal movement for FireFighter
        if not self.on_ladder and not self.climbing:
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
                moving = True
                self.facing_right = False
            
            if keys[pygame.K_d]:
                self.rect.x += self.speed
                moving = True
                self.facing_right = True
                
        #Facing Direction for the mouse
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
        
        #Extinguisher movement and contol
        if self.extinguisher_appear:
            mouse_x , mouse_y = pygame.mouse.get_pos()  
            self.facing_right = mouse_x >= self.rect.centerx
            
            mouse_buttons = pygame.mouse.get_pressed()
                
            if not self.on_ladder:
                    self.extinguisher_active = mouse_buttons[0]
            else:
                self.extinguisher_active = False
                
            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
                
            length = max(1,(dx*dx + dy*dy) ** 0.5)
            nx = dx / length
            ny = dy/length
                
            spray_length = 60
            spray_width = 20
                
            spray_x = self.rect.centerx + nx * 40
            spray_y = self.rect.centery + ny * 40
                
            self.extinguisher_rect = pygame.Rect(spray_x ,spray_y, spray_length,spray_width)
            
    def draw(self , surface):
        surface.blit(self.image , self.rect)