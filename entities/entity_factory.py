import json
import pygame
from pathlib import Path
from entities.Entity import Entity

DEFINITIONS_PATH = Path(__file__).resolve().parent / "entity_definitions.json"

def load_definitions(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)["entities"]

def make_standard_class(defn: dict) -> type:
    image_path = defn["image_path"]
    base_size  = tuple(defn["base_size"]) if defn["base_size"] else None
    scale      = defn.get("scale")        

    def __init__(self,x,y,game=None):
        Entity.__init__(self, image_path, base_size, x, y, scale=scale, game=game)

    return type(defn["name"], (Entity,), {"__init__": __init__})

def make_flip_class(defn: dict) -> type:
    image_path = defn["image_path"]
    base_size  = tuple(defn["base_size"]) if defn["base_size"] else None
    scale      = defn.get("scale")

    def __init__(self,x,y,game=None):
        Entity.__init__(self, image_path, base_size, x, y, scale=scale, game=game)
        self.image_right = self.image
        self.image_left  = pygame.transform.flip(self.image_right, True, False)
        self.image       = self.image_right

    def update(self, keys):
        pass

    return type(defn["name"], (Entity,), {"__init__": __init__, "update": update})

def make_ladder_class(defn: dict) -> type:
    image_path = defn["image_path"]
    scale = defn.get("scale", 5)

    def __init__(self,x,y,height = 200,game=None):
        base_size = (64, height)
        Entity.__init__(self, image_path, base_size, x, y, scale=scale, game=game)
        self.zone = self.rect.copy()

    return type(defn["name"], (Entity,), {"__init__": __init__})

def make_pager_class(defn: dict) -> type:
    image_path = defn["image_path"]
    base_size = tuple(defn["base_size"]) if defn["base_size"] else None
    scale = defn.get("scale", 1)
    default_time = defn.get("extras", {}).get("default_time_inside", 5)

    def __init__(self,x,y,game=None):
        Entity.__init__(self, image_path, base_size, x, y, scale=scale, game=game)
        self.time_inside = default_time
        self.pager_triggered  = False

    def start_cooldown(self):
        self.time_inside     = default_time
        self.pager_triggered = False

    def update(self, dt):
        if not self.pager_triggered:
            self.time_inside -= dt
            if self.time_inside <= 0:
                self.trigger()

    def trigger(self):
        self.game.sound_manager.stop_sound("FireCrackle")
        self.game.sound_manager.play_time_sound("PagerBeep", 2000)
        self.game.sound_manager.set_volume("PagerBeep", 0.1)
        
        self.pager_triggered = True

    def draw(self, screen):
        if self.pager_triggered:
            Entity.draw(self, screen)

    return type(
        defn["name"],
        (Entity,),
        {
            "__init__":      __init__,
            "start_cooldown": start_cooldown,
            "update":        update,
            "trigger":       trigger,
            "draw":          draw,
        },
    )

def build_class(defn: dict) -> type:
    extras = defn.get("extras", {})

    if extras.get("variable_height"):
        return make_ladder_class(defn)

    if extras.get("has_cooldown"):
        return make_pager_class(defn)

    if extras.get("flip_x"):
        return make_flip_class(defn)

    return make_standard_class(defn)

def build_object_classes(path: Path = DEFINITIONS_PATH) -> dict[str, type]:

    classes: dict[str, type] = {}
    for defn in load_definitions(path):
        cls = build_class(defn)
        classes[defn["name"]] = cls
    return classes


OBJECT_CLASSES: dict[str, type] = build_object_classes()