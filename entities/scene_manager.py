class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current = None
        
    def add(self,name,scene):
        self.scenes[name] = scene
    
    def set(self , name):
        self.current = self.scenes[name]
        if hasattr(self.current, "on_enter"):
            self.current.on_enter()
    
    def update(self , keys , dt):
        self.current.update(keys , dt)
        
    def draw(self , screen):
        self.current.draw(screen)