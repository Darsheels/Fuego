import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class UIPrompt:
    def __init__(self, text, x, y):
        # Scale font based on screen height
        font_size = int(SCREEN_HEIGHT * 0.05)   # 3% of screen height
        self.font = pygame.font.Font(None, font_size)

        self.text = text
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))

        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)