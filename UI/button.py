class Button:
    def __init__(self,x,y,image,callback):
        self.image = image
        self.rect = self.image.get_rect(topleft=(x,y))
        self.callback = callback
        self.hovered = False
        
    def update(self,mouse_pos,mouse_clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered and mouse_clicked:
            self.callback()
    
    def draw(self,screen):
        screen.blit(self.image,self.rect)