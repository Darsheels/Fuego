import pygame
from pathlib import Path
from entities.scene_manager import SceneManager
from entities.scene_factory import build_scenes_from_definitions
from scenes.animation_scenes import TruckCutsceneScene, TruckLeavingScene
from entities.entity_factory import OBJECT_CLASSES
from entities.PlayerSys import BasePlayer
from UI.MainMenu import MainMenu


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        pygame.display.set_caption("Fuego")
        self.clock   = pygame.time.Clock()
        self.running = True

        self.next_spawn  = None
        self.last_scene  = None
        self.selected_mission = None
        self.previous_mission = None

        self.base_w = 1280 
        self.base_h = 720  
        self.game_surface = pygame.Surface((self.base_w, self.base_h))

        self._scale    = 1.0
        self._offset_x = 0
        self._offset_y = 0
        self._recompute_scale()

        self.fade_state        = "none"  
        self.fade_alpha        = 0
        self.fade_speed        = 255     
        self.fade_target_scene = None
        self.fade_surface      = pygame.Surface((self.base_w, self.base_h))
        self.fade_surface.fill((0, 0, 0))

        self.fire_truck = OBJECT_CLASSES["DefaultTruck"](100, 250)
        self.pager      = OBJECT_CLASSES["Pager"](1000, 500)
        self.player     = BasePlayer(self, 400, 480, "firefighter_no_gear")

        self.scene_manager = SceneManager(self)
        self.scene_manager.add("truck_cutscene", TruckCutsceneScene(self, self.fire_truck))
        self.scene_manager.add("truck_leaving",  TruckLeavingScene(self))
        self.scene_manager.add("MainMenu",       MainMenu(self))

        definitions_path = Path(__file__).resolve().parent / "scenes" / "scene_definitions.json"
        scenes = build_scenes_from_definitions(definitions_path, self)
        for scene_name, scene in scenes.items():
            self.scene_manager.add(scene_name, scene)

        self.mission_scenes = ["FurnitureStore", "House1", "Museum", "CarCrashScene"]
        self.scene_manager.set("MainMenu")

        self.background = pygame.image.load("assets/sprites/buildingblocks/Background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.base_w, self.base_h))

        self.cursor_img  = pygame.image.load("assets/sprites/buildingblocks/MousePointer.png")
        self.cursor_rect = self.cursor_img.get_rect()

        pygame.mouse.set_visible(False)

    def _recompute_scale(self):
        win_w, win_h   = self.screen.get_size()
        self._scale    = min(win_w / self.base_w, win_h / self.base_h)
        scaled_w       = int(self.base_w * self._scale)
        scaled_h       = int(self.base_h * self._scale)
        self._offset_x = (win_w - scaled_w) // 2
        self._offset_y = (win_h - scaled_h) // 2
        print("display", win_w, win_h, "scale", self._scale,
          "scaled", scaled_w, scaled_h,
          "offset", self._offset_x, self._offset_y)
        
    def mouse_game_pos(self) :
        mx, my = pygame.mouse.get_pos()
        gx = int((mx - self._offset_x) / self._scale)
        gy = int((my - self._offset_y) / self._scale)
        gx = max(0, min(gx, self.base_w - 1))
        gy = max(0, min(gy, self.base_h - 1))
        return gx, gy

    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            self.handle_events()
            dt = self.clock.tick(60) / 1000

            self.scene_manager.update(keys, dt)
       
            self.game_surface.fill((0, 0, 0))
            self.scene_manager.draw(self.game_surface)
        
            self._update_fade(dt)
            if self.fade_state != "none":
                self.fade_surface.set_alpha(int(self.fade_alpha))
                self.game_surface.blit(self.fade_surface, (0, 0))

            scaled_w = int(self.base_w * self._scale)
            scaled_h = int(self.base_h * self._scale)
            scaled   = pygame.transform.scale(self.game_surface, (scaled_w, scaled_h))

            self.screen.fill((0, 0, 0))   
            self.screen.blit(scaled, (self._offset_x, self._offset_y))

            mx, my = pygame.mouse.get_pos()
            self.cursor_rect.center = (mx, my)
            self.screen.blit(self.cursor_img, self.cursor_rect)

            pygame.display.flip()

    def _update_fade(self, dt: float):
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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self._recompute_scale()


def main():
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()