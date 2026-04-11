import pygame
from entities.animation import load_sprite_sheet , Animation

from entities.animation import load_sprite_sheet

PLAYER_PROFILES = {
    "firefighter_no_gear": {
        "frames": ("assets/sprites/player/idleFireFighter.png", 32, 32, 7),
        "has_extinguisher": False
    },

    "firefighter_geared": {
        "frames": ("assets/sprites/player/IdleGearedFireFighter.png", 48, 96, 2),
        "has_extinguisher": False
    },

    "firefighter_with_extinguisher": {
        "frames": ("assets/sprites/player/FirefighterExtinguisher.png", 48, 96, 2),
        "has_extinguisher": True
    }
}

class BasePlayer(pygame.sprite.Sprite):
    def __init__(self,x,y,profile_name):
        super().__init__()
        self.rect = None
        
        self.speed = 2
        self.facing_right = True
        self.moving = False
        
        self.ladder = None
        self.on_ladder = False
        self.climbing = False
        self.show_ladder_prompt = False
        
        self.extinguisher_active = False
        self.extinguisher_rect = None
        self.extinguisher_appear = False
        self.has_extinguisher = True
        
        self.apply_profile(profile_name)
        
    def apply_profile(self,profile_name):
        profile = PLAYER_PROFILES[profile_name]
        path,w,h,scale = profile["frames"]
        
        self.frames = load_sprite_sheet(path,w,h,scale=scale)
        self.animation = Animation(self.frames,speed=0.1,breaker=False)
        
        self.image = self.animation
        self.rect = self.image.get_rect(topleft=self.rect.topleft)
        
        self.has_extinguisher = profile["has_extinguisher"]
        
    def update(self,keys):
        self.moving = False
    
    def update_movement(self,keys):
        pass
        
    def update_animation(self):
        pass
    
    def draw(self,screen):
        pass
            
    
    
