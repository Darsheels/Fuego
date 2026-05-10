from settings import GLOBAL_SCALE
import pygame

class Button:
    def __init__(self,x,y,image,callback,scale=None):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))
        self.callback = callback
        self.hovered = False
        self.scale = GLOBAL_SCALE if scale is None else scale
        self.image = self.scale_image(scale)
        
    def scale_image(self,scale):
        width,height = self.image.get_size()
        return pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))

    def update(self,mouse_pos,mouse_clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered and mouse_clicked:
            self.callback()
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)