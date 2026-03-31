"""
子弹实体模块
"""
import pygame
from config import PROJECTILE_CONFIG, COLORS, SCREEN_WIDTH


def get_color(name):
    if isinstance(name, tuple):
        return name
    return COLORS.get(name, (255, 255, 255))


class Pea:
    """豌豆子弹"""
    def __init__(self, x, y, row):
        self.x = x
        self.y = y
        self.row = row
        config = PROJECTILE_CONFIG["pea"]
        self.speed = config["speed"]
        self.damage = config["damage"]
        self.radius = config["radius"]
        self.alive = True
        
    def update(self, zombies):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.alive = False
            return
        for zombie in zombies:
            if zombie.alive and zombie.row == self.row:
                if abs(zombie.x - self.x) < 25 and abs(zombie.y - self.y) < 35:
                    zombie.take_damage(self.damage)
                    self.alive = False
                    break
    
    def draw(self, surface):
        pygame.draw.circle(surface, get_color("green"), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, get_color("light_green"), (int(self.x - 2), int(self.y - 2)), 3)


class SnowPeaProjectile(Pea):
    """冰豌豆"""
    def __init__(self, x, y, row):
        super().__init__(x, y, row)
        config = PROJECTILE_CONFIG["snow_pea"]
        self.slow_duration = config["slow_duration"]
        
    def update(self, zombies):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.alive = False
            return
        for zombie in zombies:
            if zombie.alive and zombie.row == self.row:
                if abs(zombie.x - self.x) < 25 and abs(zombie.y - self.y) < 35:
                    zombie.take_damage(self.damage)
                    zombie.slow_down(self.slow_duration)
                    self.alive = False
                    break
    
    def draw(self, surface):
        pygame.draw.circle(surface, get_color("accent_blue"), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (180, 220, 255), (int(self.x - 2), int(self.y - 2)), 3)
