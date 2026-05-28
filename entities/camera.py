import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self,world_width  = SCREEN_WIDTH,world_height = SCREEN_HEIGHT,lerp_speed = 6.0,deadzone_x = 80,deadzone_y = 50):
   
        self.world_width  = world_width
        self.world_height = world_height
        self.lerp_speed   = lerp_speed

        self.offset = pygame.Vector2(0, 0)

        self._dz_w = deadzone_x * 2
        self._dz_h = deadzone_y * 2
        self.deadzone = pygame.Rect(
            SCREEN_WIDTH  // 2 - deadzone_x,
            SCREEN_HEIGHT // 2 - deadzone_y,
            self._dz_w,
            self._dz_h,
        )
        
    def update(self, target_rect, dt):
        desired_x = target_rect.centerx - SCREEN_WIDTH  // 2
        desired_y = target_rect.centery - SCREEN_HEIGHT // 2

        target_screen_x = target_rect.centerx - int(self.offset.x)
        target_screen_y = target_rect.centery - int(self.offset.y)

        if self.deadzone.collidepoint(target_screen_x, target_screen_y):
            pass
        else:
            if self.lerp_speed <= 0:
                self.offset.x = desired_x
                self.offset.y = desired_y
            else:
                self.offset.x += (desired_x - self.offset.x) * min(self.lerp_speed * dt, 1.0)
                self.offset.y += (desired_y - self.offset.y) * min(self.lerp_speed * dt, 1.0)

        self._clamp()

    def _clamp(self):
        self.offset.x = max(0, min(self.offset.x, self.world_width  - SCREEN_WIDTH))
        self.offset.y = max(0, min(self.offset.y, self.world_height - SCREEN_HEIGHT))

    def apply(self, rect):
        return pygame.Rect(
            rect.x - int(self.offset.x),
            rect.y - int(self.offset.y),
            rect.width,
            rect.height,
        )

    def apply_entity(self, entity):
        return self.apply(entity.rect)

    def apply_pos(self, x, y):
        return x - self.offset.x, y - self.offset.y

    def world_to_screen(self, pos):
        return pos - self.offset

    def screen_to_world(self, pos):
        return pos + self.offset

    def draw_debug(self, screen):
        pygame.draw.rect(screen, (0, 255, 100), self.deadzone, 1)
        font = pygame.font.Font(None, 24)
        label = font.render(
            f"cam offset  x={int(self.offset.x)}  y={int(self.offset.y)}",
            True,
            (200, 200, 50),
        )
        screen.blit(label, (8, 8))
        
    @classmethod
    def single_screen(cls):
        return cls(
            world_width=SCREEN_WIDTH,
            world_height=SCREEN_HEIGHT,
            lerp_speed=0,
            deadzone_x=SCREEN_WIDTH  // 2,
            deadzone_y=SCREEN_HEIGHT // 2,
        )

    @classmethod
    def smooth_follow(cls, world_width, world_height):
        return cls(
            world_width=world_width,
            world_height=world_height,
            lerp_speed=6.0,
            deadzone_x=60,
            deadzone_y=40,
        )

    @classmethod
    def locked_follow(cls, world_width, world_height):
        return cls(
            world_width=world_width,
            world_height=world_height,
            lerp_speed=0,
            deadzone_x=0,
            deadzone_y=0,
        )