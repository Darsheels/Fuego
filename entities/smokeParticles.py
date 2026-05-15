import pygame
import random

class SmokeParticles:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        self.vx = random.uniform(-10, 10)
        self.vy = random.uniform(-1.5, -3.5)
        
        self.size = random.randint(2, 5)
        self.growth = 0.1
        
        self.alpha = 255
        self.fade_speed = random.randint(2, 5)
        
        self.color = (200, 200, 200)
        
    def update(self):
        self.x += self.vx 
        self.y += self.vy
        
        self.vx *= 0.97
        self.vx += random.uniform(-0.05, 0.05)
        self.vy -= 0.05
        
        self.size = min(self.size + 0.01, 18)
        
        self.alpha = max(0, self.alpha * 0.95)
        if self.alpha < 0:
            self.alpha = 0
        
    def draw(self, screen):
        if self.alpha > 0:
            surface = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*self.color, int(self.alpha)), (self.size, self.size), int(self.size))
            screen.blit(surface, (self.x - self.size, self.y - self.size))
            
class SmokeManager:
    def __init__(self):
        self.particles = []
        
    def add_smoke(self,x,y):
        self.particles.append(SmokeParticles(x,y))
    
    def update(self):
        for particle in self.particles:
            particle.update()
        
        self.particles = [p for p in self.particles if p.alpha > 0]
    
    def draw(self,screen):
        for particle in self.particles:
            particle.draw(screen)