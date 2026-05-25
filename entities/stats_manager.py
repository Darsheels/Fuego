import json
import os 

class StatsManager:
    def __init__(self):
        self.file_path = "./data.json"
        
        self.stats = {
            "Missions_Completed": 0,
            "People_Rescued":0,
            "Play_Time":0
        }
        self.load()
        
    def add_mission(self):
        self.stats["Missions_Completed"] += 1
    
    def add_rescued(self):
        self.stats["People_Rescued"] += 1
    
    def update_time(self,dt):
        self.stats["Play_Time"] += dt
        
    def save(self):
        os.makedirs("save", exist_ok=True)
        
        with open(self.file_path, "w") as file:
            json.dump(self.stats, file, indent=4)
    
    def load(self):
        if not os.path.exists(self.file_path):
            return
        
        with open(self.file_path, "r") as file:
            self.stats = json.load(file)