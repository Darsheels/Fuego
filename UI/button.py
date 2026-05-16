from settings import GLOBAL_SCALE
import pygame

class Button:
    def __init__(self,x,y,game,image,callback,scale=None):
        self.game = game
        self.image = image
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.callback = callback
        self.hovered = False
        self.scale = GLOBAL_SCALE if scale is None else scale
        self.image = self.scale_image(scale)
        
    def scale_image(self,scale):
        width,height = self.image.get_size()
        return pygame.transform.scale(self.image, (int(width * scale), int(height * scale))) 

    def update(self,event):
        mouse_pos = self.game.mouse_game_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.image.set_alpha(128)
        else:
            self.image.set_alpha(255)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                self.game.sound_manager.play_sound("buttonclick")
                self.callback()
               

    def draw(self,screen):
        screen.blit(self.image,self.rect)