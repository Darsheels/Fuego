import pygame
from entities.Scenes import BaseScene
from settings import SCREEN_WIDTH, SCREEN_HEIGHT


class TruckCutsceneScene(BaseScene):
    def __init__(self, game):
        super().__init__(game, None)

        # Load truck image
        self.truck = pygame.image.load("assets/truck.png").convert_alpha()
        self.truck = pygame.transform.scale(self.truck, (400, 200))

        # Start off-screen left
        self.x = -400
        self.y = SCREEN_HEIGHT * 0.6

        # Speed of animation
        self.speed = 600  # pixels per second

        # Timer for ending the cutscene
        self.timer = 0
        self.duration = 3  # seconds

    def update(self, keys, dt):
        # Move truck across screen
        self.x += self.speed * dt

        # Count time
        self.timer += dt

        # After duration → switch to fire scene
        if self.timer >= self.duration:
            self.game.scene_manager.set("fire_scene")

    def draw(self, screen):
        screen.fill((20, 20, 20))  # dark background
        screen.blit(self.truck, (self.x, self.y))