import pygame
from pathlib import Path
from entities.scene_manager import SceneManager
from entities.scene_factory import build_scenes_from_definitions
from scenes.animation_scenes import TruckCutsceneScene, TruckLeavingScene
from entities.entity_factory import OBJECT_CLASSES
from entities.PlayerSys import BasePlayer
from UI.MainMenu import MainMenu
from entities.smokeParticles import SmokeManager
from UI.button import Button
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from audio.SoundManager import SoundManager

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((0,0), pygame.NOFRAME | pygame.FULLSCREEN)
        pygame.display.set_caption("Fuego")
        self.clock   = pygame.time.Clock()
        self.running = True
        self.paused  = False

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
        self.recompute_scale()

        self.fade_state        = "none"  
        self.fade_alpha        = 0
        self.fade_speed        = 255     
        self.fade_target_scene = None
        self.fade_surface      = pygame.Surface((self.base_w, self.base_h))
        self.fade_surface.fill((0, 0, 0))

        self.fire_truck = OBJECT_CLASSES["DefaultTruck"](100, 250)
        self.pager      = OBJECT_CLASSES["Pager"](1000, 500, game=self)
        self.player     = BasePlayer(self, 400, 480, "firefighter_no_gear")
        self.smoke = SmokeManager()
        self.sound_manager = SoundManager()

        self.scene_manager = SceneManager(self)
        self.scene_manager.add("truck_cutscene", TruckCutsceneScene(self, self.fire_truck))
        self.scene_manager.add("truck_leaving",  TruckLeavingScene(self))
        self.scene_manager.add("MainMenu", MainMenu(self))

        definitions_path = Path(__file__).resolve().parent / "scenes" / "scene_definitions.json"
        scenes = build_scenes_from_definitions(definitions_path, self)
        for scene_name, scene in scenes.items():
            self.scene_manager.add(scene_name, scene)

        self.mission_scenes = ["CarCrashScene","FurnitureStore","House1","Museum",]
        self.misstion_inteiors = ["House1Int","MuseumInt","FurnitureStoreInt"]
        self.scene_manager.set("MainMenu")

        self.background = pygame.image.load("assets/sprites/buildingblocks/Background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (self.base_w, self.base_h))

        self.exit_img = pygame.image.load("assets/sprites/buildingblocks/LeaveButton.png").convert_alpha()
        self.pause_img = pygame.image.load("assets/sprites/buildingblocks/PauseButton.png").convert_alpha()
        self.settings_img = pygame.image.load("assets/sprites/buildingblocks/SettingsButton.png").convert_alpha()
        self.exit_button = Button(SCREEN_WIDTH *0.02, 40, self , self.exit_img, self.toggle_exit_menu, scale=0.8)
        self.pause_button = Button(SCREEN_WIDTH *0.02, 110, self , self.pause_img, self.toggle_pause, scale=0.8)
        self.settings_button = Button(SCREEN_WIDTH *0.02, 180, self, self.settings_img,self.toggle_setting,scale=0.8 )
        self.buttons = [self.exit_button, self.pause_button, self.settings_button]
        
        self.exitMenu_surface = pygame.image.load("assets/sprites/buildingblocks/ConfirmCancelMenu.png").convert_alpha()
        self.exitMenu_surface = pygame.transform.scale(self.exitMenu_surface, (400, 200))
        self.confirm_img = pygame.image.load("assets/sprites/buildingblocks/ConfirmButton.png").convert_alpha()
        self.cancel_img = pygame.image.load("assets/sprites/buildingblocks/CancelButton.png").convert_alpha()
        self.confirm_button = Button(SCREEN_WIDTH * 0.5 - 150, SCREEN_HEIGHT *0.5 - 35, self , self.confirm_img, self.quit_game, scale=0.8)
        self.cancel_button = Button(SCREEN_WIDTH * 0.5 + 60, SCREEN_HEIGHT *0.5 - 35, self , self.cancel_img, self.close_exit_menu, scale=0.8)
        self.menu_buttons = [self.confirm_button, self.cancel_button]
        
        self.show_exit_menu = False
        self.setting_open = False

        self.settingMenu_surface = pygame.image.load("assets/sprites/buildingblocks/SettingsMenu.png").convert_alpha()
        self.settingMenu_surface = pygame.transform.scale(self.settingMenu_surface, (200,400))
        self.MasterSound_img = pygame.image.load("assets/sprites/buildingblocks/MasterSoundSwitch.png").convert_alpha()
        self.add_img = pygame.image.load("assets/sprites/buildingblocks/Addition.png").convert_alpha()
        self.subtract_img = pygame.image.load("assets/sprites/buildingblocks/Subtraction.png").convert_alpha()        
        self.MasterSound_Button = Button(SCREEN_WIDTH * 0.12, SCREEN_HEIGHT * 0.15, self, self.MasterSound_img,self.toggle_sound,scale=0.8)
        self.add_button = Button(SCREEN_WIDTH * 0.23, SCREEN_HEIGHT * 0.25 , self,self.add_img,self.add_master_volume, scale=1)
        self.subtract_button = Button(SCREEN_WIDTH * 0.11, SCREEN_HEIGHT * 0.25, self,self.subtract_img,self.subtract_master_volume, scale=1)
        self.settings_buttons = [self.MasterSound_Button,self.add_button,self.subtract_button]
        
        self.cursor_img  = pygame.image.load("assets/sprites/buildingblocks/MousePointer.png").convert_alpha()
        self.cursor_rect = self.cursor_img.get_rect()

        pygame.mouse.set_visible(False)

    def recompute_scale(self):
        win_w, win_h = self.screen.get_size()
        self._scale = min(win_w / self.base_w, win_h / self.base_h)
        scaled_w = int(self.base_w * self._scale)
        scaled_h = int(self.base_h * self._scale)
        self._offset_x = (win_w - scaled_w) // 2
        self._offset_y = (win_h - scaled_h) // 2
        
    def mouse_game_pos(self):
        mx, my = pygame.mouse.get_pos()
        gx = int((mx - self._offset_x) / self._scale)
        gy = int((my - self._offset_y) / self._scale)
        gx = max(0, min(gx, self.base_w - 1))
        gy = max(0, min(gy, self.base_h - 1))
        return gx, gy
    
    def close_exit_menu(self):
        self.show_exit_menu = False
    
    def open_exit_menu(self):
        self.show_exit_menu = True
        
    def toggle_exit_menu(self):
        self.show_exit_menu = not self.show_exit_menu
        
    def run(self):
        while self.running:
            keys = pygame.key.get_pressed()
            self.handle_events()
            dt = self.clock.tick(60) / 1000
            
            if not self.paused:
                self.scene_manager.update(keys, dt)
       
            self.game_surface.fill((0, 0, 0))
            self.scene_manager.draw(self.game_surface)
        
            self.update_fade(dt)
            
            if self.fade_state != "none":
                self.fade_surface.set_alpha(int(self.fade_alpha))
                self.game_surface.blit(self.fade_surface, (0, 0))

            scaled_w = int(self.base_w * self._scale)
            scaled_h = int(self.base_h * self._scale)
            scaled   = pygame.transform.scale(self.game_surface, (scaled_w, scaled_h))

            self.screen.fill((0, 0, 0))   
            self.screen.blit(scaled, (self._offset_x, self._offset_y))

            self.side_buttons_update()
            self.exit_menu()
            self.paused_menu()
            self.setting_menu()
            self.sound_updates()
        
            mx, my = pygame.mouse.get_pos()
            self.cursor_rect.center = (mx, my)
            self.screen.blit(self.cursor_img, self.cursor_rect)              
            
            pygame.display.flip()

    def sound_updates(self):
        if self.scene_manager.current_name == "TruckApparatus":
            self.sound_manager.stop_sound("FireCrackle")
            self.sound_manager.stop_sound("FireTruckSiren")
            
        if self.scene_manager.current_name in self.mission_scenes:
            self.sound_manager.play_sound("Fire")
        else:
            self.sound_manager.stop_sound("Fire")
    
    def side_buttons_update(self):
        for button in self.buttons:
            if self.scene_manager.current_name != "MainMenu":   
                button.draw(self.screen)

    
    def setting_menu(self):
        if self.setting_open:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            menu_rect = self.settingMenu_surface.get_rect(bottomleft=(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.65))
            self.screen.blit(self.settingMenu_surface,menu_rect)
            
            for button in self.settings_buttons:
                button.draw(self.screen)
                
            bar_rect = pygame.Rect(SCREEN_WIDTH * 0.14,SCREEN_HEIGHT * 0.25,100,20)
            pygame.draw.rect(self.screen, (60,60,60), bar_rect)
            fill_width = int(bar_rect.width * self.sound_manager.master_volume)
            pygame.draw.rect(self.screen,(0,200,0),(bar_rect.x,bar_rect.y,fill_width,bar_rect.height))
            
    def paused_menu(self):
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(120)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            font = pygame.font.SysFont("arial", 60, bold=True)
            text = font.render("PAUSED", True, (255, 255, 255))
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(text, text_rect)
    
    def exit_menu(self):
        if self.show_exit_menu:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
                
            menu_rect = self.exitMenu_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(self.exitMenu_surface, menu_rect)
                
            for button in self.menu_buttons:
                    button.draw(self.screen)
    
    def update_fade(self, dt):
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
    
    def add_master_volume(self):
        self.sound_manager.set_master_volume(self.sound_manager.master_volume + 0.1)
        
    def subtract_master_volume(self):
        self.sound_manager.set_master_volume(self.sound_manager.master_volume - 0.1)
    
    def toggle_sound(self):
        self.sound_manager.stop_all_sounds()
        
    def quit_game(self):
        self.running = False
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def toggle_setting(self):
        self.setting_open = not self.setting_open
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.recompute_scale()
            if self.scene_manager.current_name != "MainMenu":
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.paused = not self.paused
            for button in self.buttons:
                if self.scene_manager.current_name != "MainMenu":   
                    button.update(event)
            for button in self.menu_buttons:
                if self.scene_manager.current_name != "MainMenu":  
                    button.update(event)
            for button in self.settings_buttons:
                if self.scene_manager.current_name != "MainMenu":
                    button.update(event)
            self.sound_manager.handle_event(event)

def main():
    pygame.init()
    pygame.mixer.init() 
    game = Game()
    game.run()
    pygame.quit()


if __name__ == "__main__":
    main()