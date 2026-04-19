import pygame
from entities.animation import load_sprite_sheet , Animation
import random

class Fire(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.fireFrames = load_sprite_sheet("assets/sprites/buildingblocks/Fire_animation.png", 48 , 64, scale=1)
        self.FireAnimation = Animation(self.fireFrames, speed=0.1, breaker=False)
        
        self.image = self.FireAnimation.image
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.extinguished = False
        self.extinguish_timer = 0.0
        self.extinguish_delay = 0.5
        self.spread_timer = 0
        self.spread_delay = 2
    
    def update(self,dt):
        if self.extinguished:
            return
        
        self.FireAnimation.update()
        self.spread_timer += dt
        
    def extinguish(self):
        self.extinguished = True
        self.image = pygame.Surface((0,0))
    
    def apply_extinguisher(self, dt, contacting):
        if self.extinguished:
            return
        if contacting:
            self.extinguish_timer += dt
            if self.extinguish_timer >= self.extinguish_delay:
                self.extinguish()
        else:
            self.extinguish_timer = 0.0
        
class Fire_manager:
    def __init__(self):
        self.fires = []
        
    def add_fire(self,x,y):
        self.fires.append(Fire(x,y))
    
    def update(self,dt):
        for fire in self.fires:
            fire.update(dt)
            
        self.fires = [fire for fire in self.fires if not fire.extinguished]
        
        new_fires = []
        for fire in self.fires:
            if not fire.extinguished and fire.spread_timer >= fire.spread_delay:
               if random.random() < 0.02:
                    nx = fire.rect.x + random.choice([-40,40])
                    ny = fire.rect.y + random.choice([-40,40])
                    new_fires.append(Fire(nx,ny))
                    fire.spread_timer = 0
                
        self.fires.extend(new_fires)
        
    def draw(self,screen):
        for fire in self.fires:
            screen.blit(fire.image,fire.rect)