import pygame
from settings import SCREEN_WIDTH , SCREEN_HEIGHT
from entities.UI_prompt import UIPrompt
from entities.objects import Ladder
from entities.Fire import Fire,Fire_manager
from entities.PlayerSys import BasePlayer


class BaseScene:
    def __init__(self , game , player=None, fire_truck=None, pager=None):
        self.game = game
        self.player = player
        self.fire_truck = fire_truck
        self.pager = pager
        self.objects = []
        self.prompts = []
        self.transitions = []
        self.has_pager = False
        self.fire_manager = Fire_manager()
        self.mission_accomplished = False
        self.mission_failed = False
        self.mission_popup_timer = 0
        self.is_mission_scene = False
        
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
        
        if self.is_mission_scene and not self.mission_accomplished and not self.mission_failed:
            for fire in self.fire_manager.fires:
                if not fire.can_spread and fire.has_failed():
                    self.mission_failed = True
                    self.mission_popup_timer = 2.5
                    self.game.selected_mission = None
                    break
        
        if self.mission_failed:
            self.mission_popup_timer -= dt
            if self.mission_popup_timer <= 0:
                self.game.next_spawn = "default_interior"
                self.game.scene_manager.set("TruckApparatus")
            return
        
        if self.pager:
            self.pager.update(dt)
        
        if self.scene_name == "TruckApparatus" and self.game.pager.pager_triggered and (not hasattr(self.game, 'selected_mission') or self.game.selected_mission is None):
            import random
            if hasattr(self.game, 'mission_scenes') and self.game.mission_scenes:
                available_missions = [m for m in self.game.mission_scenes if m != self.game.previous_mission]
                random_mission = random.choice(available_missions)
                self.game.previous_mission = random_mission
                self.game.selected_mission = random_mission
                if random_mission == "House1":
                    print("Selected mission: House1 - A residential fire scenario with multiple rooms and a basement.")
                else:
                    print("Selected mission: CarCrashScene - An outdoor scenario involving a vehicle fire after a crash.")
                locker_room_scene = self.game.scene_manager.scenes.get("locker_room")
                if locker_room_scene:
                    for p in locker_room_scene.prompts:
                        if p["name"] == "change into gear and exit":
                            p["target_scene"] = random_mission
                            break
        
        if self.fire_truck and self.player and getattr(self.player, "in_vehicle", False):
            actor_rect = self.fire_truck.rect
        
        elif self.player:
            actor_rect = self.player.rect
            ladder_found = False
            
            for obj in self.objects:
                if isinstance(obj,Ladder) and obj.zone.colliderect(actor_rect):
                    self.player.show_ladder_prompt = not self.player.on_ladder
                    
                    if self.player.on_ladder:
                        ladder_found = True
                        self.player.ladder = obj
                        break
                    
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
                
            if not self.mission_accomplished:
                self.player.update(keys)
            
            self.player.extinguisher_appear = len(self.fire_manager.fires) > 0 and self.is_mission_scene
            
            for fire in self.fire_manager.fires:
                contacting = self.player.extinguisher_active and self.player.extinguisher_rect and self.player.extinguisher_rect.colliderect(fire.rect)
                fire.apply_extinguisher(dt, contacting)
        
            if not self.mission_accomplished and self.is_mission_scene and len(self.fire_manager.fires) == 0:
                self.mission_accomplished = True
                self.mission_popup_timer = 2.5
        
        elif self.fire_truck:
            actor_rect = self.fire_truck.rect
            self.fire_truck.update(keys)
                
        for p in self.prompts:
            inside_zone = p["zone"].colliderect(actor_rect)
            
            if inside_zone and (p["name"] != "change into gear and exit" or self.game.pager.pager_triggered):
                p["prompt"].show()
                if p.get("type") == "interaction":
                    if keys[p["key"]]:  
                        if p["name"] == "change into gear and exit":
                            self.game.fade_target_scene = p["target"]
                            self.game.next_spawn = p["spawn"]
                            self.game.fade_state = "fading_out"
                        else:
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
    
        if self.mission_accomplished:
            self.mission_popup_timer -= dt
            if self.mission_popup_timer <= 0:
                self.game.next_spawn = "default_interior"
                self.game.scene_manager.set("TruckApparatus")
                
        
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
            
        if self.mission_accomplished:
            font = pygame.font.Font(None, 64)
            text  = font.render("Mission Accomplished!", True, (255, 215, 0))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, rect)
        elif self.mission_failed:
            font = pygame.font.Font(None, 64)
            text  = font.render("Mission Failed", True, (255, 0, 0))
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(text, rect)
     
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
        player_profile = None,
        is_mission_scene=False,
        fire_spreading=False
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
        self.is_mission_scene = is_mission_scene
        self.fire_spreading = fire_spreading
        
        if objects:
            for obj in objects:
                self.add_objects(obj)
            
        if self.fire_truck and use_shared_fire_truck:
            self.add_objects(self.fire_truck)

    def on_enter(self):
        spawn_name = self.game.next_spawn if self.game.next_spawn is not None else "default"

        if self.player:
            self.player.extinguisher_active = False
            self.player.extinguisher_rect = None
            self.player.extinguisher_appear = False
            self.player.extinguisher_pos = (0, 0)

        if self.scene_name == "TruckApparatus":
            
            if self.game.last_scene == "locker_room":
                pass
            elif self.game.last_scene:
                last = self.game.scene_manager.scenes[self.game.last_scene]
                
                if last.is_mission_scene and last.mission_accomplished:
                    print("Mission accomplished! Starting pager cooldown.")
                    self.game.pager.start_cooldown()
                    self.game.selected_mission = None
                
                else:
                    self.game.pager.time_inside = 5
                    self.game.pager.pager_triggered = False
            
            else:
                self.game.pager.time_inside = 5
                self.game.pager.pager_triggered = False

        if self.is_mission_scene:
            self.mission_accomplished = False
            self.mission_failed = False
            self.mission_popup_timer = 0
            self.mission_popup_timer = 0
            self.fire_manager.fires = [Fire(f["x"], f["y"], self.fire_spreading) for f in self.fire_defs]
                
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
