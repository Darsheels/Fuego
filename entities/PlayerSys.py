import pygame
from entities.animation import load_sprite_sheet , Animation

from entities.animation import load_sprite_sheet

PLAYER_PROFILES = {
    "firefighter_no_gear": {
        "frames": ("assets/sprites/player/idleFireFighter.png", 32, 32, 7),
        "has_extinguisher": False,
        "can_climb_ladders": True,
        "has_gear": False,
        "is_firefighter": True
    },

    "firefighter_geared": {
        "frames": ("assets/sprites/player/IdleGearedFireFighter.png", 48, 96, 2),
        "has_extinguisher": False,
        "can_climb_ladders": True,
        "has_gear": True,
        "is_firefighter": True
    },

    "firefighter_with_extinguisher": {
        "frames": ("assets/sprites/player/FirefighterExtinguisher.png", 48, 96, 2),
        "has_extinguisher": True,
        "can_climb_ladders": True,
        "has_gear": True,
        "is_firefighter": True
    }
}

class BasePlayer(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        
    def apply_profile(self,profile_name):
        profile = PLAYER_PROFILES[profile_name]
        path,w,h,scale = profile["frames"]
        
        self.frames = load_sprite_sheet(path,w,h,scale=scale)
        self.animation = Animation(self.frames,speed=0.1,breaker=False)
        
        self.image = self.animation
        
    
        
