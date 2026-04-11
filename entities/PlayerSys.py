import pygame
from entities.animation import load_sprite_sheet , Animation
from entities.animation import load_sprite_sheet

PLAYER_PROFILES = {
    "firefighter_no_gear": {
        "walk_frames": ("assets/sprites/player/DefaultPlayer.png", 32, 32, 7),
        "idle_frames": ("assets/sprites/player/idleFireFighter.png", 32,32,7),
        "has_extinguisher": False
    },

    "firefighter_geared": {
        "walk_frames": ("assets/sprites/player/Firefighter.png", 48, 96, 2),
        "idle_frames": ("assets/sprites/player/IdleGearedFireFighter.png", 48,96,2),
        "has_extinguisher": False
    },

    "firefighter_with_extinguisher": {
        "walk_frames": ("assets/sprites/player/FirefighterExtinguisher.png", 48, 96, 2),
        "idle_frames": ("assets/sprites/player/IdleFireFighterExtinguisher.png", 48,96,2),
        "has_extinguisher": True
    }
}

class BasePlayer(pygame.sprite.Sprite):
    def __init__(self,x,y,profile_name):
        super().__init__()
        self.rect = pygame.Rect(x,y,32,32)
        
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
        
        self.apply_profile(profile_name)
        
    def apply_profile(self,profile_name):
        profile = PLAYER_PROFILES[profile_name]
        wpath,ww,wh,wscale = profile["walk_frames"]
        ipath,iw,ih,iscale = profile["idle_frames"]
        
        self.walk_frames = load_sprite_sheet(wpath,ww,wh,scale=wscale)
        self.idle_frames = load_sprite_sheet(ipath,iw,ih,scale=iscale)
        
        self.walk_animation = Animation(self.walk_frames,speed=0.1,breaker=False)
        self.idle_animation = Animation(self.idle_frames,speed=0.1,breaker=False)
        
        self.image = self.idle_animation.image
        
        old_pos = self.rect.topleft
        self.rect = self.image.get_rect(topleft=old_pos)
        
        self.has_extinguisher = profile["has_extinguisher"]
        
    def update(self,keys):
        if self.on_ladder:
            self.update_ladder_logic(keys)
            
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
    
    def update_extinguisher_logic(self):
        if not self.extinguisher_appear:
            self.extinguisher_active = False
            return
        
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
    
    def draw(self,surface):
        if self.visible:
            surface.blit(self.image, self.rect)
