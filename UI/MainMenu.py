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
        
        self.play_button = Button(SCREEN_WIDTH // 2 - self.play_img.get_width() // 2, 300, self.play_img, self.start_game, scale=1.5)
        self.exit_button = Button(SCREEN_WIDTH // 2 - self.exit_img.get_width() // 2, 400, self.exit_img, self.quit_game, scale=1.5)

        self.buttons = [self.play_button, self.exit_button]

    def on_enter(self):
        pass
    
    def start_game(self):
        self.game.fade_target_scene = "TruckApparatus"
        self.game.fade_state = "fading_out"
    
    def quit_game(self):
        self.game.running = False
    
    def update(self,keys,dt):
        mouse_pos = self.game.mouse_game_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for button in self.buttons:
            button.update(mouse_pos,mouse_clicked)
    
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        for button in self.buttons:
            button.draw(screen)
