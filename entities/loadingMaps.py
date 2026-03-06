import pygame
import json

class importMap:
    def __init__(self,TileSet, Map):
        with open(Map) as f:
             self.map_data = json.load(f)
        
        self.tileset_image = pygame.image.load(TileSet).convert_alpha()
        
        self.tiles = []
        TILE_SIZE = 32
        
        tileset_width = self.tileset_image.get_width() // TILE_SIZE
        tileset_height = self.tileset_image.get_height() // TILE_SIZE
        
        for y in range(tileset_height):
            for x in range(tileset_width):
                tile = self.tileset_image.subsurface(
                    (x * TILE_SIZE, y * TILE_SIZE , TILE_SIZE , TILE_SIZE)
                )
                self.tiles.append(tile)
                
                
    def draw_tile_layer(self,screen,layer):
        tile_data = layer["data"]
        width = layer["width"]
        height = layer["height"]
        
        for i, tile_id in enumerate(tile_data):
            if tile_id == 0:
                continue
            
            tile = self.tiles[tile_id - 1]
            
            x = (i % width) * 32
            y = (i // width) * 32
            
            screen.blit(tile , (x,y))
            
    def draw(self , screen):
        
        for layer in self.map_data["layers"]:
            if layer["type"] == "tilelayer":
                self.draw_tile_layer(screen, layer)
                
        