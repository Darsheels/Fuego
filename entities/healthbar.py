import pygame

class HealthBar():
        def __init__(self, player,x, y, width=100, height=10):
            self.player = player
            self.rect = pygame.Rect(x, y, width, height)
        
        def update(self):
            self.rect.x = self.player.rect.x
            self.rect.y = self.player.rect.y - 20
            
        def draw(self, surface):
            ratio = self.player.health / 100

            pygame.draw.rect(surface, (255,0,0), self.rect)
            pygame.draw.rect(surface, (0,255,0), (self.rect.x, self.rect.y, self.rect.width * ratio, self.rect.height))