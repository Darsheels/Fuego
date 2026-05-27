from settings import GLOBAL_SCALE
import pygame

class Button:
    def __init__(self,x,y,game,image,callback,scale=None):
        self.game = game
        self.image = image
        self.callback = callback
        self.hovered = False
        self.scale = GLOBAL_SCALE if scale is None else scale
        self.image = self.scale_image(scale)
        self.rect = self.image.get_rect(topleft=(x,y))
    
    def scale_image(self,scale):
        width,height = self.image.get_size()
        
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        return pygame.transform.scale(self.image, (int(new_width), int(new_height))) 

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