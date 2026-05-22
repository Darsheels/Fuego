import pygame
import random
from entities.animation import load_sprite_sheet , Animation
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from entities.smokeParticles import SmokeManager

class Fire(pygame.sprite.Sprite):
    def __init__(self,x,y, can_spread=True,game=None):
        super().__init__()
        self.game = game
        
        self.fireFrames = load_sprite_sheet("assets/sprites/buildingblocks/NewFire_animation.png", 48 , 64, scale=2)
        self.FireAnimation = Animation(self.fireFrames, speed=0.1)
        self.image = self.FireAnimation.image
        self.rect = self.image.get_rect(topleft=(x,y))
        
        self.extinguished = False
        self.extinguish_timer = 0.0
        self.extinguish_delay = 10.0 if not can_spread else 3
        self.failure_timer = 0.0
        self.failure_limit = 20.0 if not can_spread else None
        self.spread_timer = 0
        self.spread_delay = 4
        self.can_spread = can_spread
        
        self.smoke_manager = SmokeManager()
        self.smoke_timer = 0
        self.smoke_delay = 0.1
    
    def update(self,dt):
        self.smoke_manager.update()
        if self.extinguished:
            self.game.sound_manager.stop_sound("FireCrackle")
            return
        
        self.game.sound_manager.play_sound("FireCrackle")
        
        self.smoke_timer += dt
        if self.smoke_timer >= self.smoke_delay:
            self.smoke_manager.add_smoke(self.rect.x, self.rect.y - 10)
            self.smoke_timer = 0
        
        self.FireAnimation.update()
        self.image = self.FireAnimation.image
        
        if not self.can_spread:
            self.failure_timer += dt
            
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
    def __init__(self, game):
        self.fires = []
        self.game = game
        
    def add_fire(self,x,y, can_spread=False):
        self.fires.append(Fire(x,y, can_spread, game=self.game))
    
    def update(self,dt):
        
        for fire in self.fires:
            fire.update(dt)
            
        self.fires = [fire for fire in self.fires if not fire.extinguished]
        
        new_fires = []
        for fire in self.fires:
            if not fire.extinguished and fire.can_spread and fire.spread_timer >= fire.spread_delay:
               if fire.spread_timer >= fire.spread_delay:
                    nx = fire.rect.x + random.choice([-40,40])
                    ny = fire.rect.y + random.choice([-40,40])
                    if 0 <= nx <= SCREEN_WIDTH - 48 and 0 <= ny <= SCREEN_HEIGHT - 64:
                        new_fires.append(Fire(nx,ny, can_spread=True, game=self.game))
                        fire.spread_timer = 0
                    
        self.fires.extend(new_fires)
        
    def draw(self,screen,camera=None):
        for fire in self.fires:
            fire.smoke_manager.draw(screen)
            pos = camera.apply(fire.rect) if camera else fire.rect
            screen.blit(fire.image, pos)