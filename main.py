import pygame
from pathlib import Path
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from entities.scene_manager import SceneManager
from entities.scene_factory import build_scenes_from_definitions
from scenes.animation_scenes import  TruckCutsceneScene, TruckLeavingScene 
from entities.objects import Object
from entities.PlayerSys import BasePlayer

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fuego")
        self.clock = pygame.time.Clock()
        self.running = True
        self.next_spawn = None
        self.last_scene = None 
        self.selected_mission = None
        self.previous_mission = None 
        
        # Fade transition system
        self.fade_state = "none"  # none, fading_out, fading_in
        self.fade_alpha = 0
        self.fade_speed = 255  # Alpha change per second
        self.fade_target_scene = None
        self.fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.fade_surface.fill((0, 0, 0))
        
        self.fire_truck = Object.DefaultTruck(100, 250)
        self.pager = Object.Pager(1000,500)
     
        self.player = BasePlayer(400,480,"firefighter_no_gear")
        
        self.scene_manager = SceneManager(self)
        self.scene_manager.add("truck_cutscene", TruckCutsceneScene(self, self.fire_truck))
        self.scene_manager.add("truck_leaving", TruckLeavingScene(self))

        definitions_path = Path(__file__).resolve().parent / "scenes" / "scene_definitions.json"
        scenes = build_scenes_from_definitions(definitions_path, self)
        for scene_name, scene in scenes.items():
            self.scene_manager.add(scene_name, scene)

        self.mission_scenes = ['House1', 'CarCrashScene']

        self.scene_manager.set("TruckApparatus")

        self.background = pygame.image.load("assets/sprites/buildingblocks/Background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.ground = pygame.image.load("assets/sprites/buildingblocks/Ground.png").convert_alpha()
        self.ground = pygame.transform.scale(self.ground, (SCREEN_WIDTH, 300))

    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            self.handle_events()
            dt = self.clock.tick(60) / 1000
            self.scene_manager.update(keys, dt)
            self.scene_manager.draw(self.screen)
            
            if self.fade_state == "fading_out":
                self.fade_alpha += self.fade_speed * dt
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    self.fade_state = "fading_in"
                    
                    if self.fade_target_scene:
                        self.scene_manager.set(self.fade_target_scene)
                        self.fade_target_scene = None
            elif self.fade_state == "fading_in":
                self.fade_alpha -= self.fade_speed * dt
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.fade_state = "none"
            
            
            if self.fade_state != "none":
                self.fade_surface.set_alpha(int(self.fade_alpha))
                self.screen.blit(self.fade_surface, (0, 0))
            
            pygame.display.flip()
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

if __name__ == "__main__":
    main()
     