import pygame
from entities.Scenes import BaseScene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class TruckCutsceneScene(BaseScene):
    def __init__(self, game, truck):
        super().__init__(game, None, truck)
        self.fire_truck = truck
        self.duration = 2.0
        self.elapsed = 0.0
        self.scroll_x = 0.0
        self.scroll_speed = 250

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
            # self.add_transition("House1", direction="up", spawn_point="left_entry")

    def draw(self, screen):
        x = int(self.scroll_x) % SCREEN_WIDTH
        screen.blit(self.game.background, (-x, 0))
        # screen.blit(self.game.background, (SCREEN_WIDTH - x, 0))
        screen.blit(self.game.ground, (-x, 450))
        # screen.blit(self.game.ground, (SCREEN_WIDTH - x, 450))
        self.fire_truck.draw(screen)
