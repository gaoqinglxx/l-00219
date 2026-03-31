"""
阳光实体模块
"""
import pygame
import math
from config import SUN_CONFIG, COLORS, GRID_OFFSET_Y


def get_color(name):
    if isinstance(name, tuple):
        return name
    return COLORS.get(name, (255, 255, 255))


class Sun:
    """阳光类"""
    def __init__(self, x, y, from_sky=True):
        self.x = x
        self.y = y if not from_sky else GRID_OFFSET_Y - 50
        self.target_y = y
        self.from_sky = from_sky
        self.value = SUN_CONFIG["sun_value"]
        self.radius = SUN_CONFIG["sun_radius"]
        self.alive = True
        self.lifetime = SUN_CONFIG["sun_lifetime"]
        self.speed = SUN_CONFIG["sun_fall_speed"]
        self.collected = False
        self.collect_target = (70, 25)
        
    def update(self):
        """更新阳光状态，返回收集的阳光值"""
        if self.collected:
            dx = self.collect_target[0] - self.x
            dy = self.collect_target[1] - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < 10:
                self.alive = False
                return self.value
            self.x += dx * 0.15
            self.y += dy * 0.15
        elif self.from_sky and self.y < self.target_y:
            self.y += self.speed
        else:
            self.lifetime -= 1
            if self.lifetime <= 0:
                self.alive = False
        return 0
    
    def draw(self, surface):
        """绘制阳光"""
        color = get_color("accent_yellow")
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 220, 100), (int(self.x), int(self.y)), self.radius - 5)
        # 光芒
        for i in range(8):
            angle = i * math.pi / 4
            x1 = self.x + math.cos(angle) * (self.radius + 3)
            y1 = self.y + math.sin(angle) * (self.radius + 3)
            x2 = self.x + math.cos(angle) * (self.radius + 12)
            y2 = self.y + math.sin(angle) * (self.radius + 12)
            pygame.draw.line(surface, color, (x1, y1), (x2, y2), 3)
    
    def is_clicked(self, pos):
        """检查是否被点击"""
        dx = pos[0] - self.x
        dy = pos[1] - self.y
        return dx*dx + dy*dy <= (self.radius + 10) ** 2
