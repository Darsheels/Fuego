import pygame
import random
from entities.healthbar import HealthBar
from entities.animation import Animation, load_sprite_sheet

RESCUE_RANGE   = 120   
PANIC_SPEED    = 1.2   
DIRECTION_HOLD = 60   

NPC_TYPES = [
    {
        "walk": "assets/sprites/player/NewPlayer.png",
        "idle": "assets/sprites/player/NewIdlePlayer.png"
    },
    {
        "walk": "assets/sprites/player/GirlNPCAnim.png",
        "idle": "assets/sprites/player/GirlNPCIdle.png"
    }
]

class NPC:
    def __init__(self, x, y):
        selected_NPC = random.choice(NPC_TYPES)
        self.random_NPC = selected_NPC["walk"]
        self.idle_NPC = selected_NPC["idle"]
        
        self.rect = pygame.Rect(x, y, 32, 32)
        self.speed = PANIC_SPEED
        self.visible = True

        self.health = 100
        self.max_health = 100
        self.alive = True
        self.health_bar = HealthBar(self, x, y)
        self.rescued = False

        self._dir_x = random.choice([-1, 0, 1])
        self._dir_timer = 0
        self._facing_right = True
        
        self.show_rescue_prompt = False

        self.walk_frames = load_sprite_sheet(
            self.random_NPC, 48, 96, scale=2
        )
        self.idle_frames = load_sprite_sheet(
            self.idle_NPC, 48, 96, scale=2
        )
        self.walk_anim = Animation(self.walk_frames, speed=0.1)
        self.idle_anim = Animation(self.idle_frames, speed=0.1)

        self.image = self.idle_anim.image
        old_pos = self.rect.topleft
        self.rect = self.image.get_rect(topleft=old_pos)

    def apply_fire_damage(self, dt):
        if self.rescued or not self.alive:
            return
        self.health = max(0, self.health - 15 * dt)
        if self.health <= 0:
            self.alive = False

    def set_rescued(self):
        self.rescued = True
        self.visible = False

    def update(self, dt, screen_w, screen_h):
        if self.rescued or not self.alive:
            return
        self.health_bar.update()
        self.update_wander(screen_w)
        self.update_animation()

    def update_wander(self, screen_w):
        self._dir_timer -= 1
        if self._dir_timer <= 0:
            self._dir_x = random.choice([-1, 0, 0, 1])   
            self._dir_timer = DIRECTION_HOLD + random.randint(-20, 20)

        self.rect.x += int(self._dir_x * self.speed)
        self.rect.x = max(0, min(self.rect.x, screen_w - self.rect.width))

        if self._dir_x > 0:
            self._facing_right = True
        elif self._dir_x < 0:
            self._facing_right = False

    def update_animation(self):
        moving = self._dir_x != 0
        if moving:
            self.walk_anim.update()
            frame = self.walk_anim.image
        else:
            self.idle_anim.update()
            frame = self.idle_anim.image

        self.image = frame if self._facing_right else pygame.transform.flip(frame, True, False)

    def draw(self, surface, camera=None):
        if not self.visible:
            return

        draw_rect = camera.apply(self.rect) if camera else self.rect
        surface.blit(self.image, draw_rect)

        bar_rect = pygame.Rect(draw_rect.x, draw_rect.y - 20, 60, 8)
        ratio = max(0.0, self.health / self.max_health)
        pygame.draw.rect(surface, (180, 0, 0), bar_rect)
        pygame.draw.rect(surface, (0, 220, 0),
        (bar_rect.x, bar_rect.y, int(bar_rect.width * ratio), bar_rect.height))

        if self.show_rescue_prompt:
            font = pygame.font.Font(None, 28)
            surf = font.render("Press R to rescue", True, (255, 255, 100))
            x = draw_rect.centerx - surf.get_width() // 2
            y = draw_rect.top - 40
            surface.blit(surf, (x, y))


class NPC_manager:
    def __init__(self,game):
        self.NPCs = []
        self.game = game

    def add_NPC(self, x, y):
        self.NPCs.append(NPC(x, y))

    def update(self, dt, screen_w, screen_h,fires=None, player=None, keys=None):
        fires = fires or []

        for npc in self.NPCs:
            if npc.rescued or not npc.alive:
                continue

            for fire in fires:
                if npc.rect.colliderect(fire.rect):
                    npc.apply_fire_damage(dt)

            npc.show_rescue_prompt = False
            if player and player.alive:
                dist = ((npc.rect.centerx - player.rect.centerx) ** 2 + (npc.rect.centery - player.rect.centery) ** 2) ** 0.5
                if dist <= RESCUE_RANGE:
                    npc.show_rescue_prompt = True
                    if keys and keys[pygame.K_r]:
                        self.game.stats.add_current_rescued()
                        self.game.stats.add_rescued()
                        npc.set_rescued()
                        continue

            npc.update(dt, screen_w, screen_h)

        self.NPCs = [n for n in self.NPCs if not n.rescued]

    def draw(self, screen, camera=None):
        for npc in self.NPCs:
            npc.draw(screen, camera)

    @property
    def all_alive_rescued_or_dead(self):
        return len(self.NPCs) == 0