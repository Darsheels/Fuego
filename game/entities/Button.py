import pygame

class Button:
    def __init__(self , x , y):
        self.image = pygame.image.load("assets/images/Button.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (200,200))
        self.rect = self.image.get_rect(topleft=(x,y))
        
    def draw(self,surface):
        surface.blit(self.image,self.rect)
        
    def is_clicked(self,event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
        