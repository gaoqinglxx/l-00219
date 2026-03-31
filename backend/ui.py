"""
UI渲染模块 - 界面绘制、按钮、反馈提示
"""
import pygame
import math
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, CARD_AREA_Y, CARD_AREA_HEIGHT
from config import GRID_OFFSET_X, GRID_OFFSET_Y, GRID_SIZE, ROWS, COLS

# 获取颜色
def get_color(name):
    if isinstance(name, tuple):
        return name
    return COLORS.get(name, (255, 255, 255))


# 获取字体
def get_font(names, size):
    """跨平台获取中文字体"""
    if not pygame.font.get_init():
        return None
    
    import platform
    import os
    system = platform.system()
    
    # 尝试直接加载系统字体文件（Windows）
    if system == "Windows":
        win_font_paths = [
            "C:\\Windows\\Fonts\\simhei.ttf",
            "C:\\Windows\\Fonts\\msyh.ttf",
            "C:\\Windows\\Fonts\\msyhbd.ttf",
            "C:\\Windows\\Fonts\\simsun.ttc",
            "C:\\Windows\\Fonts\\simkai.ttf",
            "C:\\Windows\\Fonts\\simfang.ttf",
        ]
        for path in win_font_paths:
            try:
                if os.path.exists(path):
                    return pygame.font.Font(path, size)
            except:
                continue
    
    # macOS: 尝试直接加载系统字体文件
    if system == "Darwin":
        mac_font_paths = [
            "/System/Library/Fonts/PingFang.ttc",
            "/System/Library/Fonts/STHeiti Light.ttc",
            "/System/Library/Fonts/STHeiti Medium.ttc",
            "/Library/Fonts/Arial Unicode.ttf",
            "/System/Library/Fonts/Hiragino Sans GB.ttc",
        ]
        for path in mac_font_paths:
            try:
                if os.path.exists(path):
                    return pygame.font.Font(path, size)
            except:
                continue
    
    # 尝试系统字体名称
    for name in names:
        try:
            # 直接尝试使用 SysFont
            font = pygame.font.SysFont(name, size)
            return font
        except:
            continue
            
    # 如果都失败，尝试使用默认字体（可能不支持中文）
    try:
        return pygame.font.Font(None, size)
    except:
        return None

# 常用中文字体列表 - 包含各平台字体
CHINESE_FONTS = [
    # Windows
    "simhei", "microsoftyahei", "microsoft yahei", "msyh", "simsun", "simkai", "simfang",
    # macOS
    "pingfangsc", "pingfang sc", "heiti sc", "stheitisc", "hiraginosansgb",
    # Linux
    "notosanscjksc", "wqyzenhei", "wenquanyizenhei", "wqy-microhei",
    # 通用
    "arialunicode", "arial unicode ms",
]

class Button:
    """按钮类"""
    def __init__(self, x, y, width, height, text, color="accent_green"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = get_color(color)
        self.hover = False
        self.font = get_font(CHINESE_FONTS, 28)
        
    def draw(self, surface):
        color = tuple(min(c + 30, 255) for c in self.color) if self.hover else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, get_color("white"), self.rect, 2, border_radius=10)
        if self.font:
            text_surf = self.font.render(self.text, True, get_color("white"))
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)


class FeedbackMessage:
    """反馈消息类 - 显示临时提示"""
    def __init__(self):
        self.messages = []  # [(text, color, timer, x, y)]
        self.font = get_font(CHINESE_FONTS, 20)
    
    def add(self, text, color="accent_yellow", duration=90, x=None, y=None):
        """添加反馈消息"""
        if x is None:
            x = SCREEN_WIDTH // 2
        if y is None:
            y = GRID_OFFSET_Y - 30
        self.messages.append({
            "text": text,
            "color": get_color(color),
            "timer": duration,
            "x": x,
            "y": y,
            "alpha": 255
        })
    
    def update(self):
        """更新消息状态"""
        for msg in self.messages[:]:
            msg["timer"] -= 1
            msg["y"] -= 0.5  # 向上飘动
            if msg["timer"] < 30:
                msg["alpha"] = int(msg["timer"] / 30 * 255)
            if msg["timer"] <= 0:
                self.messages.remove(msg)
    
    def draw(self, surface):
        """绘制所有消息"""
        if not self.font:
            return
        for msg in self.messages:
            text_surf = self.font.render(msg["text"], True, msg["color"])
            text_surf.set_alpha(msg["alpha"])
            rect = text_surf.get_rect(center=(msg["x"], msg["y"]))
            surface.blit(text_surf, rect)


def draw_health_bar(surface, x, y, current, maximum, width=40, height=6, offset_y=-45):
    """绘制血条"""
    bar_x = x - width // 2
    bar_y = y + offset_y
    ratio = max(0, current / maximum)
    
    # 背景
    pygame.draw.rect(surface, get_color("dark_gray"), 
                    (bar_x - 1, bar_y - 1, width + 2, height + 2), border_radius=3)
    
    # 血量颜色
    if ratio > 0.6:
        color = get_color("accent_green")
    elif ratio > 0.3:
        color = get_color("accent_yellow")
    else:
        color = get_color("accent_red")
    
    if ratio > 0:
        pygame.draw.rect(surface, color, 
                        (bar_x, bar_y, int(width * ratio), height), border_radius=2)


def draw_background(surface):
    """绘制游戏背景"""
    surface.fill(get_color("dark_bg"))
    
    # 草地
    for row in range(ROWS):
        for col in range(COLS):
            x = GRID_OFFSET_X + col * GRID_SIZE
            y = GRID_OFFSET_Y + row * GRID_SIZE
            color = (45, 80, 45) if (row + col) % 2 == 0 else (35, 65, 35)
            pygame.draw.rect(surface, color, (x, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, (30, 50, 30), (x, y, GRID_SIZE, GRID_SIZE), 1)
    
    # 左侧房子区域
    pygame.draw.rect(surface, (40, 35, 30), (0, GRID_OFFSET_Y, GRID_OFFSET_X - 5, ROWS * GRID_SIZE))
    pygame.draw.rect(surface, (60, 45, 35), (30, GRID_OFFSET_Y + 60, 120, 140))
    pygame.draw.polygon(surface, (80, 50, 35), 
                       [(20, GRID_OFFSET_Y + 60), (90, GRID_OFFSET_Y + 15), (160, GRID_OFFSET_Y + 60)])
    pygame.draw.rect(surface, (40, 30, 20), (70, GRID_OFFSET_Y + 130, 40, 70))
    pygame.draw.rect(surface, (80, 100, 120), (40, GRID_OFFSET_Y + 85, 28, 30))
    pygame.draw.rect(surface, (80, 100, 120), (112, GRID_OFFSET_Y + 85, 28, 30))


def draw_top_panel(surface, sun_count, wave, total_waves, fonts):
    """绘制顶部信息栏"""
    font = fonts[0] if len(fonts) > 0 else None
    
    # 顶部面板
    pygame.draw.rect(surface, get_color("dark_panel"), (0, 0, SCREEN_WIDTH, 55))
    pygame.draw.line(surface, (60, 60, 80), (0, 55), (SCREEN_WIDTH, 55), 2)
    
    # 阳光
    pygame.draw.rect(surface, get_color("dark_card"), (15, 8, 90, 40), border_radius=8)
    pygame.draw.circle(surface, get_color("accent_yellow"), (40, 28), 14)
    pygame.draw.circle(surface, (255, 220, 100), (40, 28), 10)
    if font:
        sun_text = font.render(str(sun_count), True, get_color("white"))
        surface.blit(sun_text, (62, 18))
    
    # 波数
    center_x = SCREEN_WIDTH // 2
    pygame.draw.rect(surface, get_color("dark_card"), (center_x - 60, 8, 120, 40), border_radius=8)
    if font:
        wave_text = font.render(f"波数: {wave}/{total_waves}", True, get_color("white"))
        text_rect = wave_text.get_rect(center=(center_x, 28))
        surface.blit(wave_text, text_rect)


def draw_card_area(surface, fonts):
    """绘制植物选择区域背景"""
    font_small = fonts[1] if len(fonts) > 1 else None
    
    pygame.draw.rect(surface, get_color("dark_panel"), (0, CARD_AREA_Y, SCREEN_WIDTH, CARD_AREA_HEIGHT))
    pygame.draw.line(surface, (60, 60, 80), (0, CARD_AREA_Y), (SCREEN_WIDTH, CARD_AREA_Y), 1)
    pygame.draw.line(surface, (60, 60, 80), (0, CARD_AREA_Y + CARD_AREA_HEIGHT), 
                    (SCREEN_WIDTH, CARD_AREA_Y + CARD_AREA_HEIGHT), 2)
    
    if font_small:
        title = font_small.render("选择植物", True, (150, 150, 170))
        surface.blit(title, (20, CARD_AREA_Y + 45))


def draw_game_over(surface, fonts, restart_btn, is_victory=False):
    """绘制游戏结束/胜利画面"""
    font_large = fonts[2] if len(fonts) > 2 else None
    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))
    
    if font_large:
        if is_victory:
            text = font_large.render("胜利!", True, get_color("accent_yellow"))
        else:
            text = font_large.render("游戏结束!", True, get_color("accent_red"))
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))
    
    restart_btn.draw(surface)


def draw_menu_overlay(surface, buttons, font_large):
    """绘制菜单覆盖层"""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # 半透明黑色背景
    surface.blit(overlay, (0, 0))
    
    if font_large:
        text = font_large.render("游戏菜单", True, get_color("white"))
        surface.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150))
        
    for btn in buttons:
        btn.draw(surface)


def draw_main_menu(surface, buttons, fonts):
    """绘制游戏主界面"""
    font_large = fonts[2] if len(fonts) > 2 else None
    font = fonts[0] if len(fonts) > 0 else None
    
    # 背景
    surface.fill(get_color("dark_bg"))
    
    # 绘制装饰性草地
    for row in range(8):
        for col in range(12):
            x = col * 70
            y = SCREEN_HEIGHT - 200 + row * 70
            if y >= SCREEN_HEIGHT - 200:
                color = (45, 80, 45) if (row + col) % 2 == 0 else (35, 65, 35)
                pygame.draw.rect(surface, color, (x, y, 70, 70))
    
    # 标题背景装饰
    title_y = 60
    pygame.draw.rect(surface, get_color("dark_panel"), (50, title_y - 20, SCREEN_WIDTH - 100, 100), border_radius=15)
    
    # 游戏标题
    if font_large:
        title = font_large.render("植物大战僵尸", True, get_color("accent_green"))
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, title_y))
        
        # 副标题
        if font:
            subtitle = font.render("— 简易版 —", True, get_color("gray"))
            surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, title_y + 55))
    
    # 绘制装饰植物
    _draw_menu_decorations(surface)
    
    # 绘制按钮
    for btn in buttons:
        btn.draw(surface)


def _draw_menu_decorations(surface):
    """绘制主菜单装饰元素"""
    # 左侧向日葵
    cx, cy = 80, SCREEN_HEIGHT - 120
    pygame.draw.circle(surface, (139, 90, 43), (cx, cy), 20)
    for i in range(8):
        angle = i * math.pi / 4
        px, py = cx + math.cos(angle) * 28, cy + math.sin(angle) * 28
        pygame.draw.circle(surface, get_color("accent_yellow"), (int(px), int(py)), 10)
    pygame.draw.rect(surface, get_color("dark_green"), (cx - 4, cy + 20, 8, 30))
    
    # 右侧豌豆射手
    cx, cy = SCREEN_WIDTH - 80, SCREEN_HEIGHT - 120
    pygame.draw.circle(surface, get_color("green"), (cx, cy), 24)
    pygame.draw.circle(surface, get_color("light_green"), (cx - 6, cy - 8), 8)
    pygame.draw.ellipse(surface, get_color("dark_green"), (cx + 12, cy - 8, 20, 16))
    pygame.draw.circle(surface, get_color("white"), (cx - 6, cy - 4), 8)
    pygame.draw.circle(surface, get_color("black"), (cx - 4, cy - 4), 4)
    pygame.draw.rect(surface, get_color("dark_green"), (cx - 6, cy + 20, 12, 30))
    
    # 中间僵尸
    cx, cy = SCREEN_WIDTH // 2 + 120, SCREEN_HEIGHT - 100
    # 身体
    pygame.draw.rect(surface, (80, 70, 60), (cx - 15, cy - 10, 30, 50))
    # 头
    pygame.draw.circle(surface, (120, 140, 100), (cx, cy - 30), 20)
    # 眼睛
    pygame.draw.circle(surface, get_color("white"), (cx - 7, cy - 32), 5)
    pygame.draw.circle(surface, get_color("white"), (cx + 7, cy - 32), 5)
    pygame.draw.circle(surface, get_color("accent_red"), (cx - 7, cy - 32), 2)
    pygame.draw.circle(surface, get_color("accent_red"), (cx + 7, cy - 32), 2)
