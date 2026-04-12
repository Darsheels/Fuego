import pygame
from settings import SCREEN_WIDTH , SCREEN_HEIGHT
from entities.UI_prompt import UIPrompt
from entities.objects import Ladder
from entities.Fire import Fire,Fire_manager
from entities.PlayerSys import BasePlayer


class BaseScene:
    def __init__(self , game , player=None, fire_truck=None, pager=None): #FIreFighter removed
        self.game = game
        self.player = player
        # self.fire_fighter = fire_fighter
        self.fire_truck = fire_truck
        self.pager = pager
        self.objects = []
        self.prompts = []
        self.transitions = []
        self.has_pager = False
        self.fire_manager = Fire_manager()

    def on_enter(self):
        return

    def add_objects(self, obj):
        if isinstance(obj , Fire):
            self.fire_manager.fires.append(obj)
        else:
            self.objects.append(obj)
    
    def add_transition(self, target_scene , direction , spawn_point):
        self.transitions.append({"target": target_scene , "direction": direction , "spawn": spawn_point})

    def add_interaction(self, name , text , zone , key, target_scene , spawn_point):
        prompt = UIPrompt(text, SCREEN_WIDTH * 0.5 , SCREEN_HEIGHT * 0.85)
        self.prompts.append({"name": name , "zone": zone , "prompt": prompt , "key": key , "target": target_scene , "spawn": spawn_point , "type": "interaction"})
        
    def add_pager(self):
        self.has_pager = True
        self.pager = self.game.pager
        
    def draw_ladder_prompt(self,screen):
        font = pygame.font.Font(None,32)
        text_surface = font.render("press W to climb", True, (255,255,255))
        x = self.player.rect.centerx - text_surface.get_width() // 2
        y = self.player.rect.top - 30
        screen.blit(text_surface, (x,y))
    
    def update(self , keys , dt):
        actor_rect = None
        
        self.fire_manager.update(dt)
        
        if self.pager:
            self.pager.update(dt)
        
        if self.fire_truck and self.player and getattr(self.player, "in_vehicle", False):
            actor_rect = self.fire_truck.rect
        
        elif self.player:
            actor_rect = self.player.rect
            
            ladder_found = False
            
            for obj in self.objects:
                if isinstance(obj,Ladder) and obj.zone.colliderect(actor_rect):
                    self.player.show_ladder_prompt = not self.player.on_ladder
                    
                    if keys[pygame.K_w] and not self.player.on_ladder:
                        self.player.on_ladder = True
                        self.player.ladder = obj
                        ladder_found = True
                        
                    if keys[pygame.K_s] and not self.player.on_ladder:
                        self.player.on_ladder = True
                        self.player.ladder = obj
                        ladder_found = True
            
            if not ladder_found:
                self.player.on_ladder = False
                self.player.climbing = False
                self.player.ladder = None
                self.player.show_ladder_prompt = False
            
            self.player.update(keys)
            
            self.player.extinguisher_appear = len(self.fire_manager.fires) > 0
            
            if self.player.extinguisher_active and self.player.extinguisher_rect:
                for fire in self.fire_manager.fires:
                    if self.player.extinguisher_rect.colliderect(fire.rect):
                        fire.extinguish()
            
            
           
        elif self.fire_truck:
            actor_rect = self.fire_truck.rect
            self.fire_truck.update(keys)
                
        for p in self.prompts:
            inside_zone = p["zone"].colliderect(actor_rect)
            
            if inside_zone:
                p["prompt"].show()
                if p.get("type") == "interaction":
                    if keys[p["key"]]:  
                        self.game.next_spawn = p["spawn"]
                        self.game.scene_manager.set(p["target"])

            else:
                p["prompt"].hide()
        
        for t in self.transitions:
            if actor_rect:
                if t["direction"] == "right" and actor_rect.right >= SCREEN_WIDTH:
                    self.game.next_spawn = t["spawn"]
                    self.game.scene_manager.set(t["target"])
                
                if t["direction"] == "left" and actor_rect.left <= 0:
                    self.game.next_spawn = t["spawn"]
                    self.game.scene_manager.set(t["target"])
                
                if t["direction"] == "up":
                    self.game.next_spawn = t["spawn"]
                    self.game.scene_manager.set(t["target"])
    
    
    def draw(self , screen):
        for obj in self.objects:
            obj.draw(screen)
        
        self.fire_manager.draw(screen)
            
        if self.has_pager and self.pager:
            self.pager.draw(screen)
        
        if self.player:
            self.player.draw(screen)
            if self.player.show_ladder_prompt:
                self.draw_ladder_prompt(screen)
            
        for p in self.prompts:
            p["prompt"].draw(screen)
            
     
class DataScene(BaseScene):
    def __init__(
        self,
        game,
        player=None,
        objects=None,
        scene_name=None,
        spawn_points=None,
        draw_background=False,
        draw_ground=False,
        use_shared_fire_truck=False,
        fire_truck_alignment=None,
        has_pager=False,
        player_profile = None
    ):
        super().__init__(game, player, game.fire_truck if use_shared_fire_truck else None, game.pager if has_pager else None)
        self.scene_name = scene_name
        self.spawn_points = spawn_points or {}
        self.draw_background = draw_background
        self.draw_ground = draw_ground
        self.use_shared_fire_truck = use_shared_fire_truck
        self.fire_truck_alignment = fire_truck_alignment
        self.has_pager = has_pager
        self.player_profile = player_profile

        if objects:
            for obj in objects:
                self.add_objects(obj)
            
        if self.fire_truck and use_shared_fire_truck:
            self.add_objects(self.fire_truck)

    def on_enter(self):
        spawn_name = self.game.next_spawn if self.game.next_spawn is not None else "default"

        if self.player and self.player_profile:
            self.player.apply_profile(self.player_profile)
        
        if self.player and self.scene_name in self.spawn_points:
            scene_spawns = self.spawn_points[self.scene_name]
            spawn_position = scene_spawns.get(spawn_name, scene_spawns.get("default"))
            if spawn_position:
                self.player.rect.topleft = tuple(spawn_position)

        if self.fire_truck and self.use_shared_fire_truck and self.scene_name in self.spawn_points:
            scene_spawns = self.spawn_points[self.scene_name]
            spawn_position = scene_spawns.get(spawn_name, scene_spawns.get("default"))
            if spawn_position:
                self.fire_truck.speed = 0
                if self.fire_truck_alignment == "bottom":
                    self.fire_truck.rect.x = spawn_position[0]
                    self.fire_truck.rect.bottom = 780
                else:
                    self.fire_truck.rect.topleft = tuple(spawn_position)

        if self.player and self.scene_name in self.spawn_points:
            scene_spawns = self.spawn_points[self.scene_name]
            spawn_position = scene_spawns.get(spawn_name, scene_spawns.get("default"))
            if spawn_position:
                self.player.rect.topleft = tuple(spawn_position)
        
        self.game.next_spawn = None

    def draw(self, screen):
        if self.draw_background:
            screen.blit(self.game.background, (0, 0))
        if self.draw_ground:
            screen.blit(self.game.ground, (0, 450))
        super().draw(screen)
