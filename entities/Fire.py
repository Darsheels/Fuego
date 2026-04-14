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
        
class Fire_manager:
    def __init__(self):
        self.fires = []
        
    def add_fire(self,x,y):
        self.fires.append(Fire(x,y))
    
    def update(self,dt):
        for fire in self.fires:
            fire.update(dt)
            
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