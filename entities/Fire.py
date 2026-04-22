import pygame
from entities.animation import load_sprite_sheet , Animation
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Fire(pygame.sprite.Sprite):
    def __init__(self,x,y, can_spread=True):
        super().__init__()
        self.fireFrames = load_sprite_sheet("assets/sprites/buildingblocks/Fire_animation.png", 256 , 64, scale=1)
        self.FireAnimation = Animation(self.fireFrames, speed=0.1, breaker=False)
        
        self.image = self.FireAnimation.image
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.extinguished = False
        self.extinguish_timer = 0.0
        self.extinguish_delay = 10.0 if not can_spread else 0.5
        self.failure_timer = 0.0
        self.failure_limit = 20.0 if not can_spread else None
        self.spread_timer = 0
        self.spread_delay = 2
        self.can_spread = can_spread
    
    def update(self,dt):
        if self.extinguished:
            return
        
        if not self.can_spread:
            self.failure_timer += dt
        self.FireAnimation.update()
        self.spread_timer += dt
        
    def extinguish(self):
        self.extinguished = True
        self.image = pygame.Surface((0,0))
    
    def has_failed(self):
        return self.failure_limit is not None and self.failure_timer >= self.failure_limit and not self.extinguished
    
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
        
    def add_fire(self,x,y, can_spread=False):
        self.fires.append(Fire(x,y, can_spread))
    
    def update(self,dt):
        for fire in self.fires:
            fire.update(dt)
            
        self.fires = [fire for fire in self.fires if not fire.extinguished]
        
        new_fires = []
        for fire in self.fires:
            if not fire.extinguished and fire.can_spread and fire.spread_timer >= fire.spread_delay:
               if random.random() < 0.02:
                    nx = fire.rect.x + random.choice([-40,40])
                    ny = fire.rect.y + random.choice([-40,40])
                    if 0 <= nx <= SCREEN_WIDTH - 48 and 0 <= ny <= SCREEN_HEIGHT - 64:
                        new_fires.append(Fire(nx,ny, can_spread=True))
                        fire.spread_timer = 0
                
        self.fires.extend(new_fires)
        
    def draw(self,screen):
        for fire in self.fires:
            screen.blit(fire.image,fire.rect)