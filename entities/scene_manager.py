class SceneManager:
    def __init__(self,game):
        self.game = game
        self.scenes = {}
        self.current = None
        self.current_name = None
        
    def add(self,name,scene):
        self.scenes[name] = scene
    
    def set(self , name):
        self.game.last_scene = self.current_name
        
        self.current = self.scenes[name]
        self.current_name = name
        
        if hasattr(self.current, "on_enter"):
            self.current.on_enter()
    
    def update(self , keys , dt):
        self.current.update(keys , dt)
        
    def draw(self , screen):
        self.current.draw(screen)