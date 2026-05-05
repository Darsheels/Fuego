import json
import pygame
from pathlib import Path
from entities.entity import Entity
from entities.npc import NPC

# Load definitions
_DEFINITIONS_PATH = Path(__file__).resolve().parent / "entity_definitions.json"

def _load_definitions(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)["entities"]

# Class builders
def _make_standard_class(defn: dict) -> type:
    """Return a plain Entity subclass for a standard (non-special) entity."""
    image_path = defn["image_path"]
    base_size  = tuple(defn["base_size"]) if defn["base_size"] else None
    scale      = defn.get("scale")        

    def __init__(self, x: int, y: int):
        Entity.__init__(self, image_path, base_size, x, y, scale=scale)

    return type(defn["name"], (Entity,), {"__init__": __init__})


def _make_flip_class(defn: dict) -> type:
   #  Entity that also stores a left-facing flipped image. Used by DefaultTruck (and anything else with extras.flip_x == true).
    image_path = defn["image_path"]
    base_size  = tuple(defn["base_size"]) if defn["base_size"] else None
    scale      = defn.get("scale")

    def __init__(self, x: int, y: int):
        Entity.__init__(self, image_path, base_size, x, y, scale=scale)
        self.image_right = self.image
        self.image_left  = pygame.transform.flip(self.image_right, True, False)
        self.image       = self.image_right

    def update(self, keys):
        pass

    return type(defn["name"], (Entity,), {"__init__": __init__, "update": update})


def _make_ladder_class(defn: dict) -> type:
    #Ladder takes an extra `height` argument and exposes a `zone` rect.
    image_path = defn["image_path"]
    scale      = defn.get("scale", 5)

    def __init__(self, x: int, y: int, height: int = 200):
        base_size = (64, height)
        Entity.__init__(self, image_path, base_size, x, y, scale=scale)
        self.zone = self.rect.copy()

    return type(defn["name"], (Entity,), {"__init__": __init__})


def _make_pager_class(defn: dict) -> type:
    #Pager has cooldown logic and only draws when triggered.
    image_path        = defn["image_path"]
    base_size         = tuple(defn["base_size"]) if defn["base_size"] else None
    scale             = defn.get("scale", 1)
    default_time      = defn.get("extras", {}).get("default_time_inside", 5)

    def __init__(self, x: int, y: int):
        Entity.__init__(self, image_path, base_size, x, y, scale=scale)
        self.time_inside      = default_time
        self.pager_triggered  = False

    def start_cooldown(self):
        self.time_inside     = default_time
        self.pager_triggered = False

    def update(self, dt: float):
        if not self.pager_triggered:
            self.time_inside -= dt
            if self.time_inside <= 0:
                self.trigger()

    def trigger(self):
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
    
# Router: pick the right builder for each definition

def _build_class(defn: dict) -> type:
    extras = defn.get("extras", {})

    if extras.get("variable_height"):
        return _make_ladder_class(defn)

    if extras.get("has_cooldown"):
        return _make_pager_class(defn)

    if extras.get("flip_x"):
        return _make_flip_class(defn)

    return _make_standard_class(defn)

# Public registry — built once at import time

def build_object_classes(path: Path = _DEFINITIONS_PATH) -> dict[str, type]:

    classes: dict[str, type] = {}
    for defn in _load_definitions(path):
        cls = _build_class(defn)
        classes[defn["name"]] = cls
    return classes


OBJECT_CLASSES: dict[str, type] = build_object_classes()
OBJECT_CLASSES["NPC"] = NPC 
