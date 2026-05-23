from entities.Scenes import BaseScene
from settings import SCREEN_WIDTH
from entities.animation import load_sprite_sheet, Animation

class TruckCutsceneScene(BaseScene):
    def __init__(self, game,truck): 
        super().__init__(game, None )
        self.fire_truck = truck
        self.truck_frames = load_sprite_sheet("assets/sprites/vehicles/TruckMovingAnim.png", 92,64,scale=8)
        self.truck_anim = Animation(self.truck_frames, speed=0.05)
        
        self.duration = 5.0
        self.elapsed = 0.0
        self.scroll_x = 0.0
        self.scroll_speed = 3

    def on_enter(self):
        self.elapsed = 0.0
        self.scroll_x = 0.0
        self.fire_truck.rect.topleft = (100, 270)
    

    def update(self, keys, dt):
        if self.game.scene_manager.current_name == "truck_cutscene":
            self.game.sound_manager.play_time_sound("TruckDriving", 5.0)
        
        self.elapsed += dt
        self.scroll_x += self.scroll_speed * dt
        self.truck_anim.update()
        
        self.fire_truck.image = self.truck_anim.image
        
        if self.elapsed >= self.duration:
            if self.game.selected_mission:
                self.game.scene_manager.set(self.game.selected_mission)
        
    def draw(self, screen):
        x = int(self.scroll_x) % SCREEN_WIDTH
        screen.blit(self.game.background, (-x, 0))
        self.fire_truck.draw(screen)
        

class TruckLeavingScene(BaseScene):
    def __init__(self, game):
        super().__init__(game, None)
        self.opening_scene = load_sprite_sheet("assets/sprites/vehicles/FireLeaving.png", 128, 98, scale=11)
        self.animation = Animation(self.opening_scene, speed=0.01)
        self.duration = 8.3
        self.elapsed = 0.0  
    
    def on_enter(self):
        self.elapsed = 0.0
       
    def update(self, keys, dt):
        if self.game.scene_manager.current_name == "truck_leaving":
            self.game.sound_manager.set_volume("GarageOpen", 0.2)
            self.game.sound_manager.set_volume("TruckEngine", 0.2)
            self.game.sound_manager.play_time_sound("GarageOpen", 8)
            self.game.sound_manager.play_time_sound("TruckEngine", 3)
        
        self.elapsed += dt
        self.animation.update() 
       
        if self.elapsed >= self.duration:
            self.game.scene_manager.set("truck_cutscene")
          
    def draw(self, screen): 
        screen.blit(self.game.background, (0, 0))
        screen.blit(self.animation.image, (-100 , -140))