import pygame
from entities.Scenes import BaseScene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from entities.animation import load_sprite_sheet, Animation
from entities.entity import Entity

class TruckCutsceneScene(BaseScene):
    def __init__(self, game, truck):
        super().__init__(game, None, truck)
        self.fire_truck = truck
        self.duration = 5.0
        self.elapsed = 0.0
        self.scroll_x = 0.0
        self.scroll_speed = 1

    def on_enter(self):
        self.elapsed = 0.0
        self.scroll_x = 0.0
        self.fire_truck.speed = 0
        self.fire_truck.image = self.fire_truck.image_right
        self.fire_truck.rect.topleft = (100, 250)

    def update(self, keys, dt):
        self.elapsed += dt
        self.scroll_x += self.scroll_speed * dt
        self.fire_truck.speed = 0
        self.fire_truck.rect.topleft = (100, 250)

        if self.elapsed >= self.duration:
            self.game.scene_manager.set("House1")

    def draw(self, screen):
        x = int(self.scroll_x) % SCREEN_WIDTH
        screen.blit(self.game.background, (-x, 0))
        screen.blit(self.game.ground, (-x, 450))
        self.fire_truck.draw(screen)
        

class TruckLeavingScene(BaseScene):
    def __init__(self, game):
        super().__init__(game, None)
        self.opening_scene = load_sprite_sheet("assets/sprites/vehicles/FireLeaving.png", 128, 98, scale=11)
        self.animation = Animation(self.opening_scene, speed=0.01 , breaker=True)
        self.duration = 8.0
        self.elapsed = 0.0
    
    def on_enter(self):
        self.elapsed = 0.0
       
    def update(self, keys, dt):
        self.elapsed += dt
        self.animation.update() 
       
        if self.elapsed >= self.duration:
            self.game.scene_manager.set("truck_cutscene")
          
    def draw(self, screen): 
        screen.blit(self.game.background, (0, 0))
        screen.blit(self.game.ground, (0, 450))
        screen.blit(self.animation.image, (-200 , -140))
