import json
import os 

class StatsManager:
    def __init__(self):
        self.file_path = "./data.json"
        
        self.stats = {
            "Missions_Completed": 0,
            "People_Rescued":0,
            "Play_Time":0,
            "XP": 0,
            "Rank": "Recruit",
            "Current_Mission_Rescued":0
        }
        
        self.load()
        
    def reset_current_rescued(self):
        self.stats["Current_Mission_Rescued"] = 0
        self.save()
    
    def add_current_rescued(self):
        self.stats["Current_Mission_Rescued"] += 1
        self.save()
    
    def add_mission(self):
        self.stats["Missions_Completed"] += 1
        self.update_XP()
        self.save()
    
    def add_rescued(self):
        self.stats["People_Rescued"] += 1
        self.save()
    
    def update_time(self,dt):
        self.stats["Play_Time"] += dt
        self.save()
        
    def update_XP(self):
        self.stats["XP"] += 15
        self.save()
    
    def update_Rank(self):
        if self.stats["XP"] >= 1000:
            self.stats["Rank"] = "S. Firefighter"
        elif self.stats["XP"] >= 500:
            self.stats["Rank"] = "Firefighter"
        elif self.stats["XP"] >= 100:
            self.stats["Rank"] = "P. Firefighter"
        else:
            self.stats["Rank"] = "Recruit"
    
    def save(self):
        os.makedirs("save", exist_ok=True)
        
        with open(self.file_path, "w") as file:
            json.dump(self.stats, file, indent=4)
    
    def load(self):
        if not os.path.exists(self.file_path):
            return
        
        with open(self.file_path, "r") as file:
            self.stats = json.load(file)