import pygame
import json
from pathlib import Path
from entities.Scenes import DataScene
from entities.entity_factory import OBJECT_CLASSES   

def load_scene_definitions(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        definitions = json.load(handle)
    return definitions

def _build_object(obj_def):
    obj_type = obj_def.get("class")
    if obj_type not in OBJECT_CLASSES:
        raise ValueError(f"Unknown object class in scene definition: {obj_type}")

    if obj_type == "Ladder":
        return OBJECT_CLASSES[obj_type](
            obj_def.get("x", 0),
            obj_def.get("y", 0),
            obj_def.get("height", 200),
        )

    return OBJECT_CLASSES[obj_type](obj_def.get("x", 0), obj_def.get("y", 0))

def _build_zone(zone_def):
    return pygame.Rect(zone_def["x"], zone_def["y"], zone_def["w"], zone_def["h"])


def _get_key(key_name):
    if not hasattr(pygame, key_name):
        raise ValueError(f"Unknown pygame key constant: {key_name}")
    return getattr(pygame, key_name)

def build_scene(scene_def, game):
    regular_objects = [
        obj_def for obj_def in scene_def.get("objects", [])
        if obj_def.get("class") != "Fire"
        if obj_def.get("class") != "NPC"
    ]
    objects = [_build_object(obj_def) for obj_def in regular_objects]

    scene = DataScene(
        game=game,
        player=game.player if scene_def.get("use_player", True) else None,
        objects=objects,
        scene_name=scene_def["name"],
        spawn_points=scene_def.get("spawn_points", {}),
        draw_background=scene_def.get("draw_background", False),
        use_shared_fire_truck=scene_def.get("use_shared_fire_truck", False),
        fire_truck_alignment=scene_def.get("fire_truck_alignment"),
        has_pager=scene_def.get("has_pager", False),
        player_profile=scene_def.get("player"),
        is_mission_scene=scene_def.get("is_mission_scene", False),
        fire_spreading=scene_def.get("Fire_Spreading", False)
    )

    scene.fire_defs = [
        obj_def for obj_def in scene_def.get("objects", [])
        if obj_def.get("class") == "Fire"
    ]
    
    scene.npc_defs = [
        obj_def for obj_def in scene_def.get("objects", [])
        if obj_def.get("class") == "NPC"
    ]

    for transition in scene_def.get("transitions", []):
        scene.add_transition(
            transition["target"],
            direction=transition["direction"],
            spawn_point=transition["spawn"],
        )

    for interaction in scene_def.get("interactions", []):
        scene.add_interaction(
            interaction["name"],
            interaction["text"],
            zone=_build_zone(interaction["zone"]),
            key=_get_key(interaction["key"]),
            target_scene=interaction["target_scene"],
            spawn_point=interaction["spawn_point"],
        )

    return scene

def build_scenes_from_definitions(path, game):
    definitions = load_scene_definitions(path)
    spawn_points = definitions.get("spawn_points", {})
    scenes = {}
    for scene_def in definitions.get("scenes", []):
        scene_def["spawn_points"] = spawn_points
        scenes[scene_def["name"]] = build_scene(scene_def, game)
    return scenes
