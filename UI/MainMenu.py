import random
import pygame
from UI.button import Button
from settings import SCREEN_HEIGHT,SCREEN_WIDTH

class MainMenu:
    def __init__(self,game):
        self.game = game
        self.play_img = pygame.image.load("assets/sprites/buildingblocks/PlayButton.png").convert_alpha()
        self.exit_img = pygame.image.load("assets/sprites/buildingblocks/ExitButton.png").convert_alpha()
        self.background = pygame.image.load("assets/sprites/buildingblocks/MainBackground.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.game.sound_manager.play_sound("BackgroundMusic",-1)
        self.game.sound_manager.play_sound("FireCrackle",-1)
        self.game.sound_manager.play_sound("FireTruckSiren",-1)
        
        self.play_button = Button(SCREEN_WIDTH *0.13, SCREEN_HEIGHT * 0.4, self.game, self.play_img, self.start_game, scale=1.5)
        self.exit_button = Button(SCREEN_WIDTH *0.13, SCREEN_HEIGHT * 0.55, self.game, self.exit_img, self.quit_game, scale=1.5)

        self.buttons = [self.play_button, self.exit_button]
        self.smoke_timer = 0
        
    def on_enter(self):
        pass
    
    def start_game(self):
        self.game.fade_target_scene = "TruckApparatus"
        self.game.fade_state = "fading_out"
    
    def quit_game(self):
        self.game.running = False
    
    def update(self,keys,dt):
        self.game.smoke.update()
        self.smoke_timer += dt

        if self.smoke_timer > 0.05:
            self.game.smoke.add_smoke(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT - 10)
            self.smoke_timer = 0

        for event in pygame.event.get():
            for button in self.buttons:
                button.update(event)
                
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        self.game.smoke.draw(screen)
        for button in self.buttons:
            button.draw(screen)