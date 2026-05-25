import pygame

class SoundManager:
    def __init__(self):
        self.master_volume = 1.0
        
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
            "Fire": pygame.mixer.Sound("assets/sounds/Fire.mp3"),
            "DoorBreaking": pygame.mixer.Sound("assets/sounds/DoorBreaking.mp3"),
            "Extinguishing": pygame.mixer.Sound("assets/sounds/Extinguishing.mp3")
        }
        
        self.sound_stop_event = pygame.USEREVENT + 1
        self.timed_sounds = {}
        
        self.apply_volume()
        
    def apply_volume(self):
        for sound in self.sounds.values():
            sound.set_volume(self.master_volume)

    def set_master_volume(self,volume):
        self.master_volume = max(0.0, min(1.0,volume))
        self.apply_volume()
        
    def play_sound(self, name, loop=0):
        if name in self.sounds:
            sound = self.sounds[name]
            
            for channel_id in range(pygame.mixer.get_num_channels()):
                channel = pygame.mixer.Channel(channel_id)
                
                if channel.get_sound() == sound and channel.get_busy():
                    return channel
                
            return sound.play(loops=loop)
            
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