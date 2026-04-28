import pygame

def load_sprite_sheet(path , frame_width , frame_height , scale):
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width , sheet_height = sheet.get_size()
    
    frames = []
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            if x + frame_width > sheet_width or y + frame_height > sheet_height:
                continue
            frame = sheet.subsurface(pygame.Rect(x, y, frame_width, frame_height))
            frame = pygame.transform.scale(
                frame,
                (frame_width * scale, frame_height * scale)
            )
            frames.append(frame)
            
    if not frames:
        raise ValueError(f"No frames extracted from sprite sheet {path} using {frame_width}x{frame_height}")

    return frames

class Animation:
    def __init__(self , frames , speed, loop=True):
        self.frames = frames
        self.speed = speed
        self.index = 0
        self.image = frames[0]
        self.loop = loop
        
    def update(self):
        self.index += self.speed
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]
        
       