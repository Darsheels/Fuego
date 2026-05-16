import pygame
import math
from entities.animation import load_sprite_sheet , Animation
from entities.Entity import Entity
from settings import SCREEN_WIDTH , SCREEN_HEIGHT
from entities.healthbar import HealthBar


PLAYER_PROFILES = {
    "firefighter_no_gear": {
        "walk_frames": ("assets/sprites/player/NewPlayer.png", 48, 96, 2),
        "idle_frames": ("assets/sprites/player/NewIdlePlayer.png", 48,96,2),
        "has_extinguisher": False
    },

    "firefighter_geared": {
        "walk_frames": ("assets/sprites/player/Firefighter.png", 48, 96, 2),
        "idle_frames": ("assets/sprites/player/IdleGearedFireFighter.png", 48,96,2),
        "has_extinguisher": False
    },

    "firefighter_with_extinguisher": {
        "walk_frames": ("assets/sprites/player/Firefighter.png", 48, 96, 2),
        "idle_frames": ("assets/sprites/player/IdleGearedFireFighter.png", 48,96,2),
        "has_extinguisher": True
    }
}

class BasePlayer(pygame.sprite.Sprite):
    def __init__(self,game,x,y,profile_name):
        super().__init__()
        self.rect = pygame.Rect(x,y,32,32)
        self.max_health = 100
        self.health = self.max_health
        self.alive = True
        self.healthbar = HealthBar(self,x,y)
        
        self.game = game
        self.speed = 2
        self.facing_right = True
        self.moving = False
        self.visible = True
        
        self.ladder = None
        self.on_ladder = False
        self.climbing = False
        self.show_ladder_prompt = False
        
        self.extinguisher_active = False
        self.extinguisher_rect = None
        self.extinguisher_appear = False
        self.has_extinguisher = False
        self.extinguisher = Entity("assets/sprites/buildingblocks/FireExtinguisher.png", (32,32) ,x,y, scale=3)
        self.extinguisher_rotated = self.extinguisher.image
        self.extinguisher_pos = (0, 0)
        self.beam_frames = load_sprite_sheet("assets/sprites/buildingblocks/NewExtinguisherFoamAnim.png", 64, 64, scale=3)
        self.beam_animation = Animation(self.beam_frames, speed=0.05, loop=False)
        
        self.apply_profile(profile_name)
        
    def apply_profile(self,profile_name):
        profile = PLAYER_PROFILES[profile_name]
        wpath,ww,wh,wscale = profile["walk_frames"]
        ipath,iw,ih,iscale = profile["idle_frames"]
        
        self.walk_frames = load_sprite_sheet(wpath,ww,wh,scale=wscale)
        self.idle_frames = load_sprite_sheet(ipath,iw,ih,scale=iscale)
        
        self.walk_animation = Animation(self.walk_frames,speed=0.1)
        self.idle_animation = Animation(self.idle_frames,speed=0.1)
        
        self.image = self.idle_animation.image
        
        old_pos = self.rect.topleft
        self.rect = self.image.get_rect(topleft=old_pos)
        
        self.has_extinguisher = profile["has_extinguisher"]
        
    def update(self,keys):
        
        self.healthbar.update()
            
        if self.on_ladder:
            self.moving = False
            self.update_ladder_logic(keys)
            self.update_animation()
            if self.has_extinguisher:
                self.update_extinguisher_logic()
            return
        
        if not self.on_ladder:    
            self.update_movement(keys)
            self.update_animation()

        if self.has_extinguisher:
            self.update_extinguisher_logic()
        
    def update_movement(self,keys):
        if self.on_ladder:
            return
        
        self.moving = False
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.moving = True
            self.facing_right = False
        
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.moving = True
            self.facing_right = True
            
        if self.rect.left < 0:
            self.rect.left = 0
            
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
        if self.rect.top < 0:
            self.rect.top = 0
            
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
    
    def update_animation(self):
        if self.moving:
            self.walk_animation.update()
            frame = self.walk_animation.image
        else:
            self.idle_animation.update()
            frame = self.idle_animation.image
        
        if self.facing_right:
            self.image = frame
        else:
            self.image = pygame.transform.flip(frame,True,False)    
        
    def update_ladder_logic(self,keys):
        if not self.on_ladder:
            return
        
        self.climbing = False
        self.rect.centerx = self.ladder.zone.centerx
        self.moving = False
        
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
            self.climbing = True
            self.moving = False
            
        if keys[pygame.K_s]:
            self.rect.y += self.speed
            self.climbing = True
            self.moving = False
    #Top Exit    
        if self.rect.top < self.ladder.zone.top:
            self.rect.top = self.ladder.zone.top
            self.on_ladder = False
            self.climbing = False
            self.moving = False
    #Bottom Exit
        if self.rect.bottom > self.ladder.zone.bottom:
            self.rect.bottom = self.ladder.zone.bottom
            self.on_ladder = False
            self.climbing = False
            self.moving = False
    
    def update_extinguisher_logic(self):
        if not self.extinguisher_appear:
            self.extinguisher_active = False
        
        mouse_x,mouse_y = self.game.mouse_game_pos()
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
        ny = dy /length

        angle = math.degrees(math.atan2(-dy, dx))
        
        if self.facing_right:
            self.extinguisher_rotated = pygame.transform.rotate(self.extinguisher.image, angle)
        else:
            flipped = pygame.transform.flip(self.extinguisher.image, True, False)
            self.extinguisher_rotated = pygame.transform.rotate(flipped, angle + 180)
            
        offset = self.rect.height * 0.35
        hand_x = self.rect.centerx + nx * offset
        hand_y = self.rect.centery + ny * offset
        self.extinguisher_pos = (hand_x, hand_y)
        
        nozzle_offset = 10
        start_x = hand_x + nx * nozzle_offset
        start_y = hand_y + ny * nozzle_offset
        
        beam_length = 200
        beam_width = 100
             
        beam_surface = pygame.transform.scale(self.beam_animation.image, (int(beam_length), beam_width))
        
        self.beam_rotated = pygame.transform.rotate(beam_surface, angle)
        
        center_x = start_x + nx * (beam_length / 2)
        center_y = start_y + ny * (beam_length / 2)
      
        self.extinguisher_rect = self.beam_rotated.get_rect(center=(center_x, center_y))
        
        self.extinguisher_active = mouse_buttons[0] and not self.on_ladder
        
        if self.extinguisher_active:
            self.beam_animation.update()    
        
        if not self.extinguisher_appear:
            self.extinguisher_active = False
            self.extinguisher_rect = None
    
    def draw(self,surface):
        if self.visible:
            surface.blit(self.image, self.rect)
            if self.extinguisher_active:
                surface.blit(self.beam_rotated,self.extinguisher_rect)
            if self.has_extinguisher:
                rect = self.extinguisher_rotated.get_rect(center=self.extinguisher_pos)
                surface.blit(self.extinguisher_rotated,rect)
            if self.game.selected_mission:
                self.healthbar.draw(surface)