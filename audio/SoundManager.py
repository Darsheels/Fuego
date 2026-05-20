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
            "Walking": pygame.mixer.Sound("assets/sounds/Walking.mp3"),
            "FireTruckSiren": pygame.mixer.Sound("assets/sounds/FireTruck.mp3"),
            "TruckDriving": pygame.mixer.Sound("assets/sounds/TruckDriving.mp3"),
        }
        
        self.sound_stop_event = pygame.USEREVENT + 1
        self.timed_sounds = {}
        
    def load_sound(self, name, file_path):
        self.sounds[name] = pygame.mixer.Sound(file_path)
    
    def play_sound(self, name, loop=0):
        if name in self.sounds:
            self.sounds[name].play(loops=loop)
            
    def stop_sound(self, name):
        if name in self.sounds:
            self.sounds[name].stop()
            
    def play_time_sound(self, name, duration):
        if name in self.sounds:
            sound = self.sounds[name]
            sound.play()
            
            event = self.sound_stop_event
            self.sound_stop_event += 1
           
            self.timed_sounds[event] = sound
            pygame.time.set_timer(event, int(duration * 1000), True) 
    
    def handle_event(self, event):
        if event.type in self.timed_sounds:
            self.timed_sounds[event.type].stop()
            
            pygame.time.set_timer(event.type, 0)
            del self.timed_sounds[event.type]
    
    def stop_all_sounds(self):
        pygame.mixer.stop()
        
    def set_volume(self, name, volume):
        if name in self.sounds:
            self.sounds[name].set_volume(volume)