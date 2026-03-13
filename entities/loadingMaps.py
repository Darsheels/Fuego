import pygame
import json
import xml.etree.ElementTree as ET
import os

class importMap:
    def __init__(self, Map):
        with open(Map) as f:
             self.map_data = json.load(f)
        
        self.tilesets = []
        TILE_SIZE = 32     
        SCALE = 8
        map_dir = os.path.dirname(Map)
        
        for ts in self.map_data["tilesets"]:
            
            firstgid = ts["firstgid"]
          
            tsx_path = os.path.join(map_dir, ts["source"])
            tree = ET.parse(tsx_path)
            root = tree.getroot()
            
            image_path = root.find("image").attrib["source"]
            image_path = os.path.join(os.path.dirname(tsx_path) , image_path)   
            
            
            tiles = []
            
            self.tileset_image = pygame.image.load(image_path)
        
            tileset_width = self.tileset_image.get_width() // TILE_SIZE
            tileset_height = self.tileset_image.get_height() // TILE_SIZE
            
            for y in range(tileset_height):
                for x in range(tileset_width):
                    tile = self.tileset_image.subsurface(
                        (x * TILE_SIZE, y * TILE_SIZE , TILE_SIZE , TILE_SIZE)
                    )
                    tile = pygame.transform.scale(tile , (TILE_SIZE * SCALE , TILE_SIZE * SCALE))
                    tiles.append(tile)
                    
            self.tilesets.append({
                "firstgid": firstgid,
                "lastgid": firstgid + len(tiles) - 1,
                "tiles": tiles 
            })
            
            
                
    def get_tiles(self,gid):
        if gid == 0:
            return None
        
        for ts in self.tilesets:
            if ts["firstgid"] <= gid <= ts["lastgid"]:
                Index = gid - ts["firstgid"]
                return ts["tiles"][Index]
        return None
    
    
                
    
            
    def draw(self , screen):
        TILE_SIZE = 32
        SCALE = 8
        
        for layer in self.map_data["layers"]:
            if layer["type"] != "tilelayer":
                continue
            
            tile_data = layer["data"]
            width = layer["width"]
            
            for i, gid in enumerate(tile_data):
                tile = self.get_tiles(gid)
                if tile is None:
                    continue
                
                x = (i % width) * (TILE_SIZE * SCALE)
                y = (i // width) * (TILE_SIZE * SCALE)
                screen.blit(tile, (x,y))
                
                
        