import pygame
from pathlib import Path
from settings import SCREEN_HEIGHT , SCREEN_WIDTH , FPS
from entities.Player import Player
from entities.scene_manager import SceneManager
from entities.scene_factory import build_scenes_from_definitions
# from scenes.StarterScene import FireTruckDrivingScene
from scenes.animation_scenes import TruckCutsceneScene
from entities.vehicles import DefaultTruck


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH ,SCREEN_HEIGHT))
        pygame.display.set_caption("Fuego")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.next_spawn = None
        
        self.player = Player(400 , 480)
        self.fire_truck = DefaultTruck(100,250)
        
        self.scene_manager = SceneManager()

        self.scene_manager.add("truck_cutscene", TruckCutsceneScene(self , self.fire_truck))

        definitions_path = Path(__file__).resolve().parent.parent / "scenes" / "scene_definitions.json"
        scenes = build_scenes_from_definitions(definitions_path, self)
        for scene_name, scene in scenes.items():
            self.scene_manager.add(scene_name, scene)

        # self.scene_manager.add("driving"  ,  FireTruckDrivingScene(self, self.player , self.fire_truck))

        self.scene_manager.set("fire_station_interior")
    
        self.background = pygame.image.load("assets/sprites/buildingblocks/Background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.ground = pygame.image.load("assets/sprites/buildingblocks/Ground.png").convert_alpha()
        self.ground = pygame.transform.scale(self.ground, (SCREEN_WIDTH, 300))
        
        
      
    
    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            
            self.handle_events()
            
            dt = self.clock.tick(60) / 1000
            
            self.scene_manager.update(keys , dt)
            
            self.scene_manager.draw(self.screen)
            
            pygame.display.flip()
            
            
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
      