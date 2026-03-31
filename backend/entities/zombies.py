"""
僵尸实体模块
"""
import pygame
import math
from config import ZOMBIE_CONFIG, COLORS, GRID_OFFSET_Y, GRID_SIZE
from ui import draw_health_bar


def get_color(name):
    if isinstance(name, tuple):
        return name
    return COLORS.get(name, (255, 255, 255))


class Zombie:
    """僵尸基类"""
    def __init__(self, row, config_key="normal"):
        self.row = row
        self.x = 1050  # 屏幕外
        self.y = GRID_OFFSET_Y + row * GRID_SIZE + GRID_SIZE // 2
        
        config = ZOMBIE_CONFIG.get(config_key, ZOMBIE_CONFIG["normal"])
        self.name = config.get("name", "僵尸")
        self.health = config["health"]
        self.max_health = self.health + config.get("armor_health", 0)
        self.speed = config["speed"]
        self.base_speed = self.speed
        self.damage = config["damage"]
        self.alive = True
        self.eating = False
        self.animation_frame = 0
        self.slow_timer = 0
        self.level = config.get("level", 1)
        self.enraged = False
        
    def slow_down(self, duration):
        self.slow_timer = duration
        self.speed = self.base_speed * 0.5
        
    def update(self, plants):
        self.animation_frame = (self.animation_frame + 1) % 60
        if self.slow_timer > 0:
            self.slow_timer -= 1
            if self.slow_timer <= 0:
                self.speed = self.base_speed
        
        self.eating = False
        for plant in plants:
            if plant.alive and plant.row == self.row:
                if abs(plant.x - self.x) < 35:
                    self.eating = True
                    plant.take_damage(self.damage)
                    break
        
        if not self.eating:
            self.x -= self.speed
            
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def get_total_health(self):
        return self.health
    
    def draw(self, surface):
        walk = math.sin(self.animation_frame * 0.2) * 4 if not self.eating else 0
        tint = get_color("accent_blue") if self.slow_timer > 0 else None
        body_c = tint if tint else (90, 90, 70)
        head_c = tint if tint else (140, 170, 140)
        
        pygame.draw.ellipse(surface, body_c, (self.x - 12, self.y - 8, 24, 42))
        pygame.draw.circle(surface, head_c, (int(self.x), int(self.y - 25 + walk)), 16)
        pygame.draw.circle(surface, get_color("white"), (int(self.x - 5), int(self.y - 27 + walk)), 5)
        pygame.draw.circle(surface, get_color("white"), (int(self.x + 5), int(self.y - 27 + walk)), 5)
        pygame.draw.circle(surface, get_color("accent_red"), (int(self.x - 5), int(self.y - 27 + walk)), 2)
        pygame.draw.circle(surface, get_color("accent_red"), (int(self.x + 5), int(self.y - 27 + walk)), 2)
        
        arm = math.sin(self.animation_frame * 0.3) * 8
        pygame.draw.line(surface, head_c, (self.x - 12, self.y), (self.x - 28, self.y - 16 + arm), 5)
        pygame.draw.line(surface, head_c, (self.x + 12, self.y), (self.x + 28, self.y - 16 - arm), 5)
        
        leg = math.sin(self.animation_frame * 0.2) * 6
        pygame.draw.line(surface, (70, 70, 50), (self.x - 6, self.y + 30), (self.x - 10 + leg, self.y + 45), 5)
        pygame.draw.line(surface, (70, 70, 50), (self.x + 6, self.y + 30), (self.x + 10 - leg, self.y + 45), 5)
        
        draw_health_bar(surface, self.x, self.y, self.get_total_health(), self.max_health, 
                       width=30, height=5, offset_y=-48)


class ConeheadZombie(Zombie):
    """路障僵尸"""
    def __init__(self, row):
        super().__init__(row, "conehead")
        config = ZOMBIE_CONFIG["conehead"]
        self.armor_health = config["armor_health"]
        self.max_health = self.health + self.armor_health
        
    def take_damage(self, damage):
        if self.armor_health > 0:
            self.armor_health -= damage
            if self.armor_health < 0:
                self.health += self.armor_health
                self.armor_health = 0
        else:
            self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def get_total_health(self):
        return self.health + self.armor_health
    
    def draw(self, surface):
        super().draw(surface)
        if self.armor_health > 0:
            walk = math.sin(self.animation_frame * 0.2) * 4 if not self.eating else 0
            pts = [(self.x, self.y - 52 + walk), 
                   (self.x - 14, self.y - 28 + walk), 
                   (self.x + 14, self.y - 28 + walk)]
            pygame.draw.polygon(surface, (255, 140, 50), pts)
            pygame.draw.polygon(surface, (200, 100, 30), pts, 2)


class BucketheadZombie(Zombie):
    """铁桶僵尸"""
    def __init__(self, row):
        super().__init__(row, "buckethead")
        config = ZOMBIE_CONFIG["buckethead"]
        self.armor_health = config["armor_health"]
        self.max_health = self.health + self.armor_health
        
    def take_damage(self, damage):
        if self.armor_health > 0:
            self.armor_health -= damage
            if self.armor_health < 0:
                self.health += self.armor_health
                self.armor_health = 0
        else:
            self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def get_total_health(self):
        return self.health + self.armor_health
    
    def draw(self, surface):
        super().draw(surface)
        if self.armor_health > 0:
            walk = math.sin(self.animation_frame * 0.2) * 4 if not self.eating else 0
            pygame.draw.rect(surface, get_color("gray"), (self.x - 14, self.y - 45 + walk, 28, 24))
            pygame.draw.rect(surface, (100, 100, 100), (self.x - 14, self.y - 45 + walk, 28, 24), 2)


class FootballZombie(Zombie):
    """橄榄球僵尸"""
    def __init__(self, row):
        super().__init__(row, "football")
        config = ZOMBIE_CONFIG["football"]
        self.armor_health = config["armor_health"]
        self.max_health = self.health + self.armor_health
        
    def take_damage(self, damage):
        if self.armor_health > 0:
            self.armor_health -= damage
            if self.armor_health < 0:
                self.health += self.armor_health
                self.armor_health = 0
        else:
            self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def get_total_health(self):
        return self.health + self.armor_health
    
    def draw(self, surface):
        walk = math.sin(self.animation_frame * 0.2) * 4 if not self.eating else 0
        tint = get_color("accent_blue") if self.slow_timer > 0 else None
        
        # 橄榄球身体
        body_c = tint if tint else (180, 50, 50)
        pygame.draw.ellipse(surface, body_c, (self.x - 15, self.y - 5, 30, 45))
        pygame.draw.rect(surface, body_c, (self.x - 8, self.y - 30, 16, 25))
        
        # 头盔
        head_c = tint if tint else (80, 80, 80)
        pygame.draw.ellipse(surface, head_c, (self.x - 18, self.y - 40 + walk, 36, 30))
        pygame.draw.ellipse(surface, (60, 60, 60), (self.x - 15, self.y - 35 + walk, 30, 22))
        
        # 面甲
        pygame.draw.rect(surface, (255, 255, 255), (self.x - 12, self.y - 35 + walk, 24, 10), 2)
        
        # 护肩
        pygame.draw.rect(surface, (200, 200, 200), (self.x - 20, self.y, 40, 8))
        pygame.draw.rect(surface, (150, 150, 150), (self.x - 18, self.y - 5, 36, 10), 2)
        
        # 四肢
        arm = math.sin(self.animation_frame * 0.3) * 8
        pygame.draw.line(surface, (180, 50, 50), (self.x - 15, self.y + 5), (self.x - 30, self.y - 10 + arm), 6)
        pygame.draw.line(surface, (180, 50, 50), (self.x + 15, self.y + 5), (self.x + 30, self.y - 10 - arm), 6)
        
        leg = math.sin(self.animation_frame * 0.2) * 6
        pygame.draw.line(surface, (150, 40, 40), (self.x - 8, self.y + 35), (self.x - 15 + leg, self.y + 50), 6)
        pygame.draw.line(surface, (150, 40, 40), (self.x + 8, self.y + 35), (self.x + 15 - leg, self.y + 50), 6)
        
        draw_health_bar(surface, self.x, self.y, self.get_total_health(), self.max_health, 
                       width=30, height=5, offset_y=-55)


class NewspaperZombie(Zombie):
    """读报僵尸"""
    def __init__(self, row):
        super().__init__(row, "newspaper")
        config = ZOMBIE_CONFIG["newspaper"]
        self.armor_health = config["armor_health"]
        self.max_health = self.health + self.armor_health
        self.rage_speed = config["rage_speed"]
        self.rage_damage = config["rage_damage"]
        
    def take_damage(self, damage):
        if self.armor_health > 0:
            self.armor_health -= damage
            if self.armor_health < 0:
                self.health += self.armor_health
                self.armor_health = 0
                # 报纸被打破，进入狂暴状态
                self.enraged = True
                self.speed = self.rage_speed
                self.base_speed = self.rage_speed
                self.damage = self.rage_damage
        else:
            self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def get_total_health(self):
        return self.health + self.armor_health
    
    def draw(self, surface):
        walk = math.sin(self.animation_frame * 0.2) * 4 if not self.eating else 0
        tint = get_color("accent_blue") if self.slow_timer > 0 else None
        
        # 基础身体
        body_c = tint if tint else (90, 90, 70)
        head_c = tint if tint else (140, 170, 140)
        
        if self.enraged:
            # 狂暴状态 - 更暴躁的外观
            body_c = (120, 50, 50) if not tint else tint
            head_c = (180, 80, 80) if not tint else tint
            walk = walk * 2  # 更疯狂的动作
            
        pygame.draw.ellipse(surface, body_c, (self.x - 12, self.y - 8, 24, 42))
        pygame.draw.circle(surface, head_c, (int(self.x), int(self.y - 25 + walk)), 16)
        
        # 眼睛
        eye_color = get_color("accent_red") if self.enraged else get_color("accent_red")
        pygame.draw.circle(surface, get_color("white"), (int(self.x - 5), int(self.y - 27 + walk)), 5)
        pygame.draw.circle(surface, get_color("white"), (int(self.x + 5), int(self.y - 27 + walk)), 5)
        pygame.draw.circle(surface, eye_color, (int(self.x - 5), int(self.y - 27 + walk)), 2)
        pygame.draw.circle(surface, eye_color, (int(self.x + 5), int(self.y - 27 + walk)), 2)
        
        # 报纸
        if self.armor_health > 0:
            pygame.draw.rect(surface, (240, 230, 210), (self.x - 20, self.y - 35 + walk, 40, 30))
            pygame.draw.rect(surface, (200, 190, 170), (self.x - 18, self.y - 33 + walk, 36, 26), 2)
            # 报纸文字
            for i in range(4):
                pygame.draw.line(surface, (100, 100, 100), 
                               (self.x - 16, self.y - 30 + i * 6 + walk),
                               (self.x + 16, self.y - 30 + i * 6 + walk), 1)
        
        # 四肢
        arm = math.sin(self.animation_frame * 0.3) * 8
        if self.enraged:
            arm = arm * 2
        pygame.draw.line(surface, head_c, (self.x - 12, self.y), (self.x - 28, self.y - 16 + arm), 5)
        pygame.draw.line(surface, head_c, (self.x + 12, self.y), (self.x + 28, self.y - 16 - arm), 5)
        
        leg = math.sin(self.animation_frame * 0.2) * 6
        if self.enraged:
            leg = leg * 2
        pygame.draw.line(surface, (70, 70, 50), (self.x - 6, self.y + 30), (self.x - 10 + leg, self.y + 45), 5)
        pygame.draw.line(surface, (70, 70, 50), (self.x + 6, self.y + 30), (self.x + 10 - leg, self.y + 45), 5)
        
        draw_health_bar(surface, self.x, self.y, self.get_total_health(), self.max_health, 
                       width=30, height=5, offset_y=-48)


class DancerZombie(Zombie):
    """跳舞僵尸"""
    def __init__(self, row):
        super().__init__(row, "dancer")
        
    def draw(self, surface):
        walk = math.sin(self.animation_frame * 0.2) * 4 if not self.eating else 0
        tint = get_color("accent_blue") if self.slow_timer > 0 else None
        
        # 跳舞动作
        dance_offset = math.sin(self.animation_frame * 0.1) * 6
        
        # 身体
        body_c = tint if tint else (100, 80, 60)
        head_c = tint if tint else (160, 180, 160)
        
        pygame.draw.ellipse(surface, body_c, (self.x - 14, self.y - 10, 28, 45))
        pygame.draw.circle(surface, head_c, (int(self.x), int(self.y - 30 + walk + dance_offset)), 18)
        
        # 眼睛
        pygame.draw.circle(surface, get_color("white"), (int(self.x - 5), int(self.y - 32 + walk + dance_offset)), 6)
        pygame.draw.circle(surface, get_color("white"), (int(self.x + 5), int(self.y - 32 + walk + dance_offset)), 6)
        pygame.draw.circle(surface, get_color("accent_red"), (int(self.x - 5), int(self.y - 32 + walk + dance_offset)), 3)
        pygame.draw.circle(surface, get_color("accent_red"), (int(self.x + 5), int(self.y - 32 + walk + dance_offset)), 3)
        
        # 帽子
        pygame.draw.rect(surface, (50, 50, 50), (self.x - 15, self.y - 45 + walk + dance_offset, 30, 10))
        pygame.draw.rect(surface, (30, 30, 30), (self.x - 12, self.y - 55 + walk + dance_offset, 24, 12))
        
        # 跳舞的手臂动作
        arm1_angle = self.animation_frame * 0.15
        arm2_angle = self.animation_frame * 0.15 + math.pi
        
        arm1_x = self.x + math.cos(arm1_angle) * 25
        arm1_y = self.y + math.sin(arm1_angle) * 15 - 5
        arm2_x = self.x + math.cos(arm2_angle) * 25
        arm2_y = self.y + math.sin(arm2_angle) * 15 - 5
        
        pygame.draw.line(surface, head_c, (self.x - 15, self.y), (arm1_x - 15, arm1_y), 5)
        pygame.draw.line(surface, head_c, (self.x + 15, self.y), (arm2_x + 15, arm2_y), 5)
        
        # 腿部
        leg = math.sin(self.animation_frame * 0.2) * 8
        pygame.draw.line(surface, (80, 60, 40), (self.x - 8, self.y + 30), (self.x - 15 + leg, self.y + 48), 6)
        pygame.draw.line(surface, (80, 60, 40), (self.x + 8, self.y + 30), (self.x + 15 - leg, self.y + 48), 6)
        
        draw_health_bar(surface, self.x, self.y, self.get_total_health(), self.max_health, 
                       width=30, height=5, offset_y=-65)
