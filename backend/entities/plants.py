"""
植物实体模块
"""
import pygame
import math
import random
from config import PLANT_CONFIG, COLORS, GRID_OFFSET_X, GRID_OFFSET_Y, GRID_SIZE
from ui import draw_health_bar
from .sun import Sun
from .projectiles import Pea, SnowPeaProjectile


def get_color(name):
    if isinstance(name, tuple):
        return name
    return COLORS.get(name, (255, 255, 255))


class Plant:
    """植物基类"""
    def __init__(self, row, col, config_key="sunflower"):
        self.row = row
        self.col = col
        self.x = GRID_OFFSET_X + col * GRID_SIZE + GRID_SIZE // 2
        self.y = GRID_OFFSET_Y + row * GRID_SIZE + GRID_SIZE // 2
        
        config = PLANT_CONFIG.get(config_key, {})
        self.name = config.get("name", "植物")
        self.cost = config.get("cost", 50)
        self.health = config.get("health", 100)
        self.max_health = self.health
        self.alive = True
        self.animation_frame = 0
        
    def update(self, zombies, projectiles, suns):
        self.animation_frame = (self.animation_frame + 1) % 120
    
    def draw(self, surface):
        pass
    
    def draw_health(self, surface):
        if self.health < self.max_health:
            draw_health_bar(surface, self.x, self.y, self.health, self.max_health, 
                           width=35, height=5, offset_y=-40)
    
    def draw_name(self, surface):
        """绘制植物中文名称"""
        from ui import get_font, CHINESE_FONTS, get_color
        font = get_font(CHINESE_FONTS, 14)
        if font:
            text_surf = font.render(self.name, True, get_color("white"))
            text_rect = text_surf.get_rect(center=(self.x, self.y - 55))
            surface.blit(text_surf, text_rect)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False


class Sunflower(Plant):
    """向日葵"""
    def __init__(self, row, col):
        super().__init__(row, col, "sunflower")
        config = PLANT_CONFIG["sunflower"]
        self.sun_timer = 0
        self.sun_interval = config["sun_interval"]
        
    def update(self, zombies, projectiles, suns):
        super().update(zombies, projectiles, suns)
        self.sun_timer += 1
        if self.sun_timer >= self.sun_interval:
            self.sun_timer = 0
            # 阳光落在向日葵所在单元格内
            suns.append(Sun(self.x, self.y + 10, from_sky=False))
    
    def draw(self, surface):
        bob = math.sin(self.animation_frame * 0.1) * 2
        green = get_color("dark_green")
        pygame.draw.rect(surface, green, (self.x - 4, self.y + 8, 8, 20))
        pygame.draw.ellipse(surface, get_color("green"), (self.x - 20, self.y + 12, 16, 8))
        pygame.draw.ellipse(surface, get_color("green"), (self.x + 4, self.y + 12, 16, 8))
        pygame.draw.circle(surface, get_color("brown"), (int(self.x), int(self.y - 3 + bob)), 18)
        pygame.draw.circle(surface, (80, 50, 30), (int(self.x), int(self.y - 3 + bob)), 12)
        for i in range(10):
            angle = i * math.pi / 5 + self.animation_frame * 0.02
            px = self.x + math.cos(angle) * 22
            py = self.y - 3 + bob + math.sin(angle) * 22
            pygame.draw.circle(surface, get_color("accent_yellow"), (int(px), int(py)), 8)
        self.draw_health(surface)
        self.draw_name(surface)


class Peashooter(Plant):
    """豌豆射手"""
    def __init__(self, row, col):
        super().__init__(row, col, "peashooter")
        config = PLANT_CONFIG["peashooter"]
        self.shoot_timer = 0
        self.shoot_interval = config["shoot_interval"]
        
    def update(self, zombies, projectiles, suns):
        super().update(zombies, projectiles, suns)
        has_zombie = any(z.row == self.row and z.x > self.x for z in zombies if z.alive)
        if has_zombie:
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                projectiles.append(Pea(self.x + 25, self.y - 8, self.row))
    
    def draw(self, surface):
        bob = math.sin(self.animation_frame * 0.15) * 2
        green = get_color("green")
        dark_green = get_color("dark_green")
        light_green = get_color("light_green")
        pygame.draw.rect(surface, dark_green, (self.x - 6, self.y + 4, 12, 24))
        pygame.draw.ellipse(surface, green, (self.x - 24, self.y + 8, 20, 10))
        pygame.draw.ellipse(surface, green, (self.x + 4, self.y + 8, 20, 10))
        pygame.draw.circle(surface, green, (int(self.x), int(self.y - 8 + bob)), 20)
        pygame.draw.circle(surface, light_green, (int(self.x - 4), int(self.y - 12 + bob)), 6)
        pygame.draw.ellipse(surface, dark_green, (self.x + 12, self.y - 14 + bob, 16, 12))
        pygame.draw.ellipse(surface, get_color("black"), (self.x + 14, self.y - 12 + bob, 10, 8))
        pygame.draw.circle(surface, get_color("white"), (int(self.x - 6), int(self.y - 14 + bob)), 6)
        pygame.draw.circle(surface, get_color("black"), (int(self.x - 4), int(self.y - 14 + bob)), 3)
        self.draw_health(surface)
        self.draw_name(surface)


class SnowPea(Plant):
    """寒冰射手"""
    def __init__(self, row, col):
        super().__init__(row, col, "snowpea")
        config = PLANT_CONFIG["snowpea"]
        self.shoot_timer = 0
        self.shoot_interval = config["shoot_interval"]
        
    def update(self, zombies, projectiles, suns):
        super().update(zombies, projectiles, suns)
        has_zombie = any(z.row == self.row and z.x > self.x for z in zombies if z.alive)
        if has_zombie:
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_interval:
                self.shoot_timer = 0
                projectiles.append(SnowPeaProjectile(self.x + 25, self.y - 8, self.row))
    
    def draw(self, surface):
        bob = math.sin(self.animation_frame * 0.15) * 2
        blue = get_color("accent_blue")
        pygame.draw.rect(surface, (0, 80, 120), (self.x - 6, self.y + 4, 12, 24))
        pygame.draw.ellipse(surface, blue, (self.x - 24, self.y + 8, 20, 10))
        pygame.draw.ellipse(surface, blue, (self.x + 4, self.y + 8, 20, 10))
        pygame.draw.circle(surface, blue, (int(self.x), int(self.y - 8 + bob)), 20)
        pygame.draw.circle(surface, (180, 220, 255), (int(self.x - 4), int(self.y - 12 + bob)), 6)
        pygame.draw.ellipse(surface, (0, 80, 120), (self.x + 12, self.y - 14 + bob, 16, 12))
        pygame.draw.ellipse(surface, (30, 50, 80), (self.x + 14, self.y - 12 + bob, 10, 8))
        pygame.draw.circle(surface, get_color("white"), (int(self.x - 6), int(self.y - 14 + bob)), 6)
        pygame.draw.circle(surface, (0, 40, 80), (int(self.x - 4), int(self.y - 14 + bob)), 3)
        self.draw_health(surface)
        self.draw_name(surface)


class WallNut(Plant):
    """坚果墙"""
    def __init__(self, row, col):
        super().__init__(row, col, "wallnut")
        
    def draw(self, surface):
        shake = math.sin(self.animation_frame * 0.05) * 1
        ratio = self.health / self.max_health
        if ratio > 0.6:
            color, dark = (200, 170, 130), (170, 140, 100)
        elif ratio > 0.3:
            color, dark = (170, 140, 100), (140, 110, 70)
        else:
            color, dark = (130, 80, 40), (100, 50, 20)
        pygame.draw.ellipse(surface, color, (self.x - 20 + shake, self.y - 25, 40, 55))
        pygame.draw.ellipse(surface, dark, (self.x - 15 + shake, self.y - 20, 30, 45))
        pygame.draw.circle(surface, get_color("white"), (int(self.x - 8 + shake), int(self.y - 8)), 6)
        pygame.draw.circle(surface, get_color("white"), (int(self.x + 8 + shake), int(self.y - 8)), 6)
        pygame.draw.circle(surface, get_color("black"), (int(self.x - 6 + shake), int(self.y - 8)), 3)
        pygame.draw.circle(surface, get_color("black"), (int(self.x + 10 + shake), int(self.y - 8)), 3)
        pygame.draw.arc(surface, get_color("black"), (self.x - 8 + shake, self.y + 2, 16, 12), 0, math.pi, 2)
        self.draw_health(surface)
        self.draw_name(surface)


class CherryBomb(Plant):
    """樱桃炸弹"""
    def __init__(self, row, col):
        super().__init__(row, col, "cherrybomb")
        config = PLANT_CONFIG["cherrybomb"]
        self.timer = config["explosion_delay"]
        self.explosion_damage = config["explosion_damage"]
        self.explosion_range = config["explosion_range"]
        self.exploded = False
        
    def update(self, zombies, projectiles, suns):
        self.timer -= 1
        if self.timer <= 0 and not self.exploded:
            self.exploded = True
            for zombie in zombies:
                if abs(zombie.row - self.row) <= 1:
                    if abs(zombie.x - self.x) <= GRID_SIZE * self.explosion_range:
                        zombie.take_damage(self.explosion_damage)
            self.alive = False
    
    def draw(self, surface):
        shake = random.randint(-3, 3) if self.timer < 30 else 0
        red = get_color("accent_red")
        pygame.draw.circle(surface, red, (int(self.x - 12 + shake), int(self.y + shake)), 18)
        pygame.draw.circle(surface, red, (int(self.x + 12 + shake), int(self.y + shake)), 18)
        pygame.draw.circle(surface, (255, 120, 120), (int(self.x - 16 + shake), int(self.y - 6 + shake)), 5)
        pygame.draw.circle(surface, (255, 120, 120), (int(self.x + 8 + shake), int(self.y - 6 + shake)), 5)
        dark_green = get_color("dark_green")
        pygame.draw.line(surface, dark_green, (self.x - 12 + shake, self.y - 16 + shake), 
                        (self.x + shake, self.y - 28 + shake), 3)
        pygame.draw.line(surface, dark_green, (self.x + 12 + shake, self.y - 16 + shake), 
                        (self.x + shake, self.y - 28 + shake), 3)
        pygame.draw.circle(surface, get_color("white"), (int(self.x - 16 + shake), int(self.y - 1 + shake)), 5)
        pygame.draw.circle(surface, get_color("white"), (int(self.x + 8 + shake), int(self.y - 1 + shake)), 5)
        pygame.draw.circle(surface, get_color("black"), (int(self.x - 14 + shake), int(self.y - 1 + shake)), 2)
        pygame.draw.circle(surface, get_color("black"), (int(self.x + 10 + shake), int(self.y - 1 + shake)), 2)
        self.draw_name(surface)
