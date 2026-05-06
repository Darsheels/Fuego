import pygame
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from entities.UI_prompt import UIPrompt
from entities.entity_factory import OBJECT_CLASSES
from entities.Fire import Fire, Fire_manager
from entities.npc import NPC, NPC_manager
from entities.camera import Camera


class Interaction:
    """Replaces the raw prompt dict — easier to inspect in a debugger."""
    def __init__(self, name, text, zone, key, target_scene, spawn_point):
        self.name        = name
        self.zone        = zone
        self.key         = key
        self.target      = target_scene
        self.spawn       = spawn_point
        self.uses_fade   = name in ("change into gear and exit", "Break in", "Break")
        self.prompt      = UIPrompt(text, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.85)

    def __repr__(self):
        return f"<Interaction '{self.name}' → '{self.target}'>"


class BaseScene:
    def __init__(self, game, player=None, fire_truck=None, pager=None):
        self.game         = game
        self.player       = player
        self.fire_truck   = fire_truck
        self.pager        = pager
        self.objects      = []
        self.interactions : list[Interaction] = []
        self.transitions  = []
        self.has_pager    = False
        self.fire_manager = Fire_manager()
        self.npc_manager  = NPC_manager()
        self.camera       = Camera.single_screen()

        self.is_mission_scene     = False
        self.mission_accomplished = False
        self.mission_failed       = False
        self.mission_popup_timer  = 0.0

    def on_enter(self):
        pass

    def add_objects(self, obj):
        if isinstance(obj, Fire):
            self.fire_manager.fires.append(obj)
        elif isinstance(obj, NPC):
            self.npc_manager.NPCs.append(obj)
        else:
            self.objects.append(obj)

    def add_transition(self, target_scene, direction, spawn_point):
        self.transitions.append({
            "target": target_scene,
            "direction": direction,
            "spawn": spawn_point,
        })

    def add_interaction(self, name, text, zone, key, target_scene, spawn_point):
        self.interactions.append(
            Interaction(name, text, zone, key, target_scene, spawn_point)
        )

    def add_pager(self):
        self.has_pager = True
        self.pager = self.game.pager


    def update(self, keys, dt):
        self.fire_manager.update(dt)

        # NPC manager: pass fires, player, and keys so it can handle
        # fire damage, rescue prompts, and the R-key rescue all in one place.
        self.npc_manager.update(dt,screen_w=SCREEN_WIDTH,screen_h=SCREEN_HEIGHT,fires=self.fire_manager.fires,player=self.player if self.player and self.player.alive else None,keys=keys,)

        for obj in self.objects:
            if hasattr(obj, "update") and callable(obj.update):
                obj.update(keys)

        if self.player:
            self.camera.update(self.player.rect, dt)

        self._check_mission_failure(dt)
        if self.mission_failed:
            self._tick_mission_popup(dt, failed=True)
            return

        if self.pager:
            self.pager.update(dt)

        self._select_mission()

        actor_rect = self._update_actor(keys, dt)

        self._update_interactions(keys, actor_rect)
        self._update_transitions(actor_rect)

        if self.mission_accomplished:
            self._tick_mission_popup(dt, failed=False)


    def draw(self, screen):
        for obj in self.objects:
            if obj.image:
                screen.blit(obj.image, self.camera.apply(obj.rect))
            else:
                obj.draw(screen)

        self.fire_manager.draw(screen, self.camera)
        self.npc_manager.draw(screen, self.camera)

        if self.has_pager and self.pager:
            self.pager.draw(screen)

        if self.player:
            original_topleft = self.player.rect.topleft
            self.player.rect.topleft = self.camera.apply(self.player.rect).topleft
            self.player.draw(screen)
            self.player.rect.topleft = original_topleft

            if self.player.show_ladder_prompt:
                self._draw_ladder_prompt(screen)

        for ix in self.interactions:
            ix.prompt.draw(screen)

        self._draw_mission_overlay(screen)

  
    # Mission failure / success
    def _check_mission_failure(self, dt):
     #Trigger mission failure when a fire burns out, an NPC dies, or the player dies.
        if not self.is_mission_scene:
            return
        if self.mission_accomplished or self.mission_failed:
            return

        # Fire failure (non-spreading fires that timed out)
        for fire in self.fire_manager.fires:
            if not fire.can_spread and fire.has_failed():
                self._fail_mission()
                return

        # NPC failure — any NPC that is dead (health == 0) and not rescued
        for npc in self.npc_manager.NPCs:
            if not npc.alive:
                self._fail_mission()
                return

        # Player death
        if self.player and self.player.health <= 0:
            self._fail_mission()

    def _fail_mission(self):
        self.mission_failed      = True
        self.mission_popup_timer = 2.5
        self.game.selected_mission = None

    def _tick_mission_popup(self, dt, *, failed: bool):
        #Count down the result banner then return to base.
        self.mission_popup_timer -= dt
        if self.mission_popup_timer <= 0:
            self.game.next_spawn = "default_interior"
            self.game.scene_manager.set("TruckApparatus")

    def _check_mission_accomplished(self):
        #       Mission is complete when:
        #   - All fires are extinguished, AND
        #   - All NPCs have been rescued (npc_manager list is empty because
        #     rescued NPCs are pruned immediately).
        
        if not self.is_mission_scene:
            return
        if self.mission_accomplished or self.mission_failed:
            return
        fires_clear = len(self.fire_manager.fires) == 0
        npcs_clear  = len(self.npc_manager.NPCs) == 0
        if fires_clear and npcs_clear:
            self.mission_accomplished = True
            self.mission_popup_timer  = 2.5

    
    # Mission selection
    def _select_mission(self):
        #Pick a random mission when the pager fires on the TruckApparatus scene.
        if self.scene_name != "TruckApparatus":
            return
        if not self.game.pager.pager_triggered:
            return
        if self.game.selected_mission:
            return
        if not getattr(self.game, "mission_scenes", None):
            return

        available = [m for m in self.game.mission_scenes
                     if m != self.game.previous_mission]
        chosen = random.choice(available)
        self.game.previous_mission = chosen
        self.game.selected_mission = chosen
        print(f"[mission] Selected: {chosen}")


    # Actor update
    def _update_actor(self, keys, dt) -> pygame.Rect | None:
        if self.fire_truck and self.player and getattr(self.player, "in_vehicle", False):
            return self.fire_truck.rect

        if self.player:
            return self._update_player(keys, dt)

        if self.fire_truck:
            self.fire_truck.update(keys)
            return self.fire_truck.rect

        return None

    def _update_player(self, keys, dt) -> pygame.Rect:
        actor_rect = self.player.rect

        # Fire damage to player
        for fire in self.fire_manager.fires:
            if actor_rect.colliderect(fire.rect):
                self.player.health = max(0, self.player.health - 20 * dt)
                if self.player.health == 0:
                    self.player.alive = False

        self._update_ladder(keys, actor_rect)

        if not self.mission_accomplished:
            self.player.update(keys)

        # Extinguisher visibility — only show when fires exist in a mission
        self.player.extinguisher_appear = (
            bool(self.fire_manager.fires) and self.is_mission_scene
        )

        # Apply extinguisher to fires
        for fire in self.fire_manager.fires:
            hitting = (
                self.player.extinguisher_active
                and self.player.extinguisher_rect is not None
                and self.player.extinguisher_rect.colliderect(fire.rect)
            )
            fire.apply_extinguisher(dt, hitting)

        # Check mission complete (fires AND npcs)
        self._check_mission_accomplished()

        return actor_rect

  
    # Ladder
    def _update_ladder(self, keys, actor_rect):
        ladder_found = False

        for obj in self.objects:
            if not isinstance(obj, OBJECT_CLASSES["Ladder"]):
                continue
            if not obj.zone.colliderect(actor_rect):
                continue

            self.player.show_ladder_prompt = not self.player.on_ladder

            if self.player.on_ladder:
                self.player.ladder = obj
                ladder_found = True
                break

            if keys[pygame.K_w] or keys[pygame.K_s]:
                self.player.on_ladder = True
                self.player.ladder    = obj
                ladder_found          = True
                break

        if not ladder_found:
            self.player.on_ladder         = False
            self.player.climbing          = False
            self.player.ladder            = None
            self.player.show_ladder_prompt = False

    
    # Interactions / transitions
    def _update_interactions(self, keys, actor_rect):
        if actor_rect is None:
            return

        for ix in self.interactions:
            inside = ix.zone.colliderect(actor_rect)
            visible = inside and (
                ix.name != "change into gear and exit"
                or self.game.pager.pager_triggered
            )

            if visible:
                ix.prompt.show()
                if keys[ix.key]:
                    self._trigger_interaction(ix)
            else:
                ix.prompt.hide()

    def _trigger_interaction(self, ix: "Interaction"):
        if ix.uses_fade:
            self.game.fade_target_scene = ix.target
            self.game.next_spawn        = ix.spawn
            self.game.fade_state        = "fading_out"
        else:
            self.game.next_spawn = ix.spawn
            self.game.scene_manager.set(ix.target)

    def _update_transitions(self, actor_rect):
        if actor_rect is None:
            return

        for t in self.transitions:
            direction = t["direction"]
            if direction == "right" and actor_rect.right >= SCREEN_WIDTH:
                self._go(t)
            elif direction == "left" and actor_rect.left <= 0:
                self._go(t)
            elif direction == "up":
                self._go(t)

    def _go(self, transition: dict):
        self.game.next_spawn = transition["spawn"]
        self.game.scene_manager.set(transition["target"])

    
    # Drawing helpers
    
    def _draw_ladder_prompt(self, screen):
        font = pygame.font.Font(None, 32)
        surf = font.render("Press W to climb", True, (255, 255, 255))
        x = self.player.rect.centerx - surf.get_width() // 2
        y = self.player.rect.top - 30
        screen.blit(surf, (x, y))

    def _draw_mission_overlay(self, screen):
        if self.mission_accomplished:
            self._draw_banner(screen, "Mission Accomplished!", (255, 215, 0))
        elif self.mission_failed:
            self._draw_banner(screen, "Mission Failed", (255, 0, 0))

    @staticmethod
    def _draw_banner(screen, text: str, color: tuple):
        font = pygame.font.Font(None, 64)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(surf, rect)


class DataScene(BaseScene):
    def __init__(
        self,
        game,
        player=None,
        objects=None,
        scene_name=None,
        spawn_points=None,
        draw_background=False,
        use_shared_fire_truck=False,
        fire_truck_alignment=None,
        has_pager=False,
        player_profile=None,
        is_mission_scene=False,
        fire_spreading=False,
    ):
        super().__init__(
            game,
            player,
            game.fire_truck if use_shared_fire_truck else None,
            game.pager      if has_pager             else None,
        )
        self.scene_name            = scene_name
        self.spawn_points          = spawn_points or {}
        self.draw_background       = draw_background
        self.use_shared_fire_truck = use_shared_fire_truck
        self.fire_truck_alignment  = fire_truck_alignment
        self.has_pager             = has_pager
        self.player_profile        = player_profile
        self.is_mission_scene      = is_mission_scene
        self.fire_spreading        = fire_spreading
        self.fire_defs             = []   # populated by scene_factory
        self.npc_defs              = []   # populated by scene_factory

        for obj in (objects or []):
            self.add_objects(obj)

        if self.fire_truck and use_shared_fire_truck:
            self.add_objects(self.fire_truck)


    def on_enter(self):
        spawn_name = self.game.next_spawn or "default"

        self._reset_player_extinguisher()
        self._handle_truck_apparatus_entry()

        if self.is_mission_scene:
            self._reset_mission()

        if self.player and not self.is_mission_scene:
            self.player.health = self.player.max_health
            self.player.alive  = True

        if self.player and self.player_profile:
            self.player.apply_profile(self.player_profile)

        self._place_player(spawn_name)
        self._place_fire_truck(spawn_name)

        self.game.next_spawn = None


    def _reset_player_extinguisher(self):
        if not self.player:
            return
        self.player.extinguisher_active = False
        self.player.extinguisher_rect   = None
        self.player.extinguisher_appear = False
        self.player.extinguisher_pos    = (0, 0)

    def _handle_truck_apparatus_entry(self):
        if self.scene_name != "TruckApparatus":
            return

        last_name = self.game.last_scene
        if last_name == "locker_room":
            return

        pager = self.game.pager
        if last_name:
            last = self.game.scene_manager.scenes[last_name]
            if last.is_mission_scene and last.mission_accomplished:
                print("[pager] Mission complete — starting cooldown.")
                pager.start_cooldown()
                self.game.selected_mission = None
                return

        pager.time_inside     = 5
        pager.pager_triggered = False

    def _reset_mission(self):
        #Rebuild fires and NPCs from their definitions every time the scene is entered.
        self.player.health        = 100
        self.mission_accomplished = False
        self.mission_failed       = False
        self.mission_popup_timer  = 0.0

        self.fire_manager.fires = [
            Fire(f["x"], f["y"], self.fire_spreading)
            for f in self.fire_defs
        ]
        self.npc_manager.NPCs = [
            NPC(n["x"], n["y"])
            for n in self.npc_defs
        ]

    def _get_spawn_position(self, spawn_name: str):
        scene_spawns = self.spawn_points.get(self.scene_name, {})
        return scene_spawns.get(spawn_name) or scene_spawns.get("default")

    def _place_player(self, spawn_name: str):
        if not self.player:
            return
        pos = self._get_spawn_position(spawn_name)
        if pos:
            self.player.rect.topleft = tuple(pos)

    def _place_fire_truck(self, spawn_name: str):
        if not (self.fire_truck and self.use_shared_fire_truck):
            return
        pos = self._get_spawn_position(spawn_name)
        if not pos:
            return
        self.fire_truck.speed = 0
        if self.fire_truck_alignment == "bottom":
            self.fire_truck.rect.x      = pos[0]
            self.fire_truck.rect.bottom = 780
        else:
            self.fire_truck.rect.topleft = tuple(pos)

    def draw(self, screen):
        if self.draw_background:
            screen.blit(self.game.background, (0, 0))
        super().draw(screen)
