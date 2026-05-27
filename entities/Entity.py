import pygame
from settings import GLOBAL_SCALE

class Entity:
    def __init__(self, image_path=None, base_size=None, x=0, y=0, scale=None,game=None):
        self.game = game
        self.image_path = image_path
        self.base_size = base_size
        self.scale = GLOBAL_SCALE if scale is None else scale
        self.world_pos = pygame.Vector2(x, y)
        self.image = None
        self.rect = pygame.Rect(x, y, 0, 0)

        if self.image_path:
            self.rescale()

    @staticmethod
    def load_scaled_image(image_path, width, height, scale):
        image = pygame.image.load(image_path).convert_alpha()
        if width is None or height is None:
            width, height = image.get_size()
        return pygame.transform.scale(image, (int(width * scale), int(height * scale)))

    def rescale(self):
        if self.base_size is None:
            loaded_image = pygame.image.load(self.image_path).convert_alpha()
            width, height = loaded_image.get_size()
        else:
            width, height = self.base_size

        self.image = self.load_scaled_image(self.image_path, width, height, self.scale)
        self.rect = self.image.get_rect(topleft=(self.world_pos.x, self.world_pos.y))

    def set_position(self, x, y):
        self.world_pos.update(x, y)
        self.rect.topleft = (x, y)

    def draw(self, surface,camera=None):
        if camera:
            surface.blit(self.image,camera.apply(self.rect))
        else:
            surface.blit(self.image,self.rect)