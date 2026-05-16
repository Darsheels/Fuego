import pygame

class SoundManager:
    def __init__(self):
        self.sounds = {
            "buttonclick": pygame.mixer.Sound("assets/sounds/ButtonClick.mp3"),
            "FireCrackle": pygame.mixer.Sound("assets/sounds/FireCrackling.mp3"),
            "BackgroundMusic": pygame.mixer.Sound("assets/sounds/MainMenuBackground.mp3"),
            "PagerBeep": pygame.mixer.Sound("assets/sounds/PagerBeep.mp3"),
            "TruckEngine": pygame.mixer.Sound("assets/sounds/TruckStarting.mp3"),
            "GarageOpen": pygame.mixer.Sound("assets/sounds/GarageDoorOpening.mp3"),
        }
    
    def load_sound(self, name, file_path):
        self.sounds[name] = pygame.mixer.Sound(file_path)
    
    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()
            
    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()
    
    def stop_all_sounds(self):
        pygame.mixer.stop()
        
    def set_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)