import pygame
import random
from entities.healthbar import HealthBar
from entities.animation import Animation, load_sprite_sheet
from settings import SCREEN_HEIGHT,SCREEN_WIDTH

class NPC:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,32,32)
        self.speed = 2
        self.visible = True
        
        self.health = 100
        self.alive = True
        self.health_bar = HealthBar(self,x,y)        
        self.rescued = False
        
        self.walk_frames = load_sprite_sheet("assets/sprites/player/NewPlayer.png", 48,96,2)
        self.idle_frames = load_sprite_sheet("assets/sprites/player/NewIdlePlayer.png",48,96,2)
        
        self.walk_anim = Animation(self.walk_frames,speed=0.1)
        self.idle_anim = Animation(self.idle_frames, speed=0.1)
        
        self.image = self.idle_anim.image
        
        old_pos = self.rect.topleft
        self.rect = self.image.get_rect(topleft=old_pos)
        
    def update(self,keys):
        if self.rescued:
            return
        
        self.health_bar.update()
        self.update_movement()
        self.update_animation()
        
    def update_movement(self):
        self.direction_x = random.choice([-1, 0, 1])
        self.rect.x += self.direction_x
        
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
        if self.rect.top < 0:
            self.rect.top = 0
            
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def update_animation(self):
        self.walk_anim.update()
        frame = self.walk_anim.image
                    
    def set_rescued(self):
        self.rescued = True
        self.visible = False
        
    def draw(self,surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            self.health_bar.draw(surface)