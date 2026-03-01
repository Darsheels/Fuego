import pygame

def load_sprite_sheet(path , frame_width , frame_height , scale = 7):
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width , sheet_height = sheet.get_size()
    
    frames = []
    for x in range(0 , sheet_width , frame_width):
        frame  = sheet.subsurface(pygame.Rect(x , 0 ,frame_width , frame_height))
        frame = pygame.transform.scale(
            frame ,
            (frame_width * scale , frame_height * scale) 
        )
        
        frames.append(frame)
        
    return frames



class Animation:
    def __init__(self , frames , speed):
        self.frames = frames
        self.speed = speed
        self.index = 0
        self.image = frames[0]
        
    def update(self):
        self.index += self.speed
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
        