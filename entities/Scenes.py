import pygame
from entities.pager import Pager
from settings import SCREEN_WIDTH , SCREEN_HEIGHT
from entities.UI_prompt import UIPrompt

class BaseScene:
    def __init__(self , game , player):
        self.game = game
        self.player = player
        self.objects = []
        self.prompts = []
        self.transitions = []
        self.has_pager = False

    
    def add_objects(self, obj):
        self.objects.append(obj)
    
    def add_transition(self, target_scene , direction , spawn_point):
        self.transitions.append({"target": target_scene , "direction": direction , "spawn": spawn_point})

    def add_interaction(self, name , text , zone , key, target_scene , spawn_point):
        prompt = UIPrompt(text, SCREEN_WIDTH * 0.5 , SCREEN_HEIGHT * 0.85)
        self.prompts.append({"name": name , "zone": zone , "prompt": prompt , "key": key , "target": target_scene , "spawn": spawn_point , "type": "interaction"})
        
    def add_pager(self):
        self.has_pager = True
        self.pager = Pager(1000,500)
        
    def update(self , keys , dt):
        self.player.update(keys)
        
        if self.has_pager:
            self.pager.update(dt)
            
        for p in self.prompts:
            inside_zone =  p["zone"].colliderect(self.player.rect)
            
            if inside_zone:
                p["prompt"].show()
                if p.get("type") == "interaction":
                    if keys[p["key"]]:  
                        self.game.next_spawn = p["spawn"]
                        self.game.scene_manager.set(p["target"])

            else:
                p["prompt"].hide()
                
        for t in self.transitions:
            if t["direction"] == "right" and self.player.rect.right >= SCREEN_WIDTH:
                self.game.next_spawn = t["spawn"]
                self.game.scene_manager.set(t["target"])
            
            if t["direction"] == "left" and self.player.rect.left <= 0:
                self.game.next_spawn = t["spawn"]
                self.game.scene_manager.set(t["target"])
    
    def draw(self , screen):
        for obj in self.objects:
            obj.draw(screen)
            
        if self.has_pager:
            self.pager.draw(screen)
        
        self.player.draw(screen)
        
        for p in self.prompts:
            p["prompt"].draw(screen)