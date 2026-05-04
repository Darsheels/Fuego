import pygame
import random
from entities.healthbar import HealthBar
from entities.animation import Animation, load_sprite_sheet

class NPC:
    def __init__(self,x,y):
        self.rect = pygame.Rect(x,y,32,48)
        self.speed = 2
        
        self.health = 100
        self.alive = True
        self.health_bar = HealthBar(self,x,y)        
        self.rescued = False
        
        self.walk_frames = load_sprite_sheet("assets/sprites/player/NewPlayer.png", 48,96,2)
        self.idle_frames = load_sprite_sheet("assets/sprites/player/NewIdlePlayer.png",48,96,2)
        
        self.walk_anim = Animation(self.walk_frames,speed=0.1)
        self.idle_anim = Animation(self.idle_frames, speed=0.1)
        
    def update(self,player,dt):
        if self.rescued:
            return
        
        self.rect.x += random.randint(-1,1)        
        self.rect.x -= random.randint(-1,1)
        
    def rescued(self):
        self.rescued = True
        
        
    def draw(self,screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
    
        