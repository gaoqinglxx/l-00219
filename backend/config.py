"""
游戏配置文件 - 所有数值配置集中管理
"""

# 网格设置
GRID_SIZE = 70
ROWS = 5
COLS = 9

# UI布局
CARD_AREA_Y = 55
CARD_AREA_HEIGHT = 110

# 网格偏移 - 根据内容自动计算
GRID_OFFSET_X = 160  # 左侧房子区域宽度
GRID_OFFSET_Y = CARD_AREA_Y + CARD_AREA_HEIGHT + 10  # 卡片区域下方

# 屏幕设置 - 根据实际内容计算，减少空白
SCREEN_WIDTH = GRID_OFFSET_X + COLS * GRID_SIZE + 20  # 右侧留20像素边距
SCREEN_HEIGHT = GRID_OFFSET_Y + ROWS * GRID_SIZE + 30  # 底部留30像素边距
FPS = 60

# 颜色配置 - 暗色系
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "dark_bg": (25, 25, 35),
    "dark_panel": (35, 35, 50),
    "dark_card": (45, 45, 65),
    "accent_green": (80, 200, 120),
    "accent_blue": (100, 150, 255),
    "accent_yellow": (255, 200, 50),
    "accent_red": (255, 80, 80),
    "gray": (128, 128, 128),
    "dark_gray": (60, 60, 70),
    "green": (60, 180, 60),
    "dark_green": (40, 120, 40),
    "light_green": (120, 220, 120),
    "brown": (139, 90, 60),
}

# 植物配置
PLANT_CONFIG = {
    "sunflower": {
        "name": "向日葵",
        "cost": 50,
        "health": 100,
        "sun_interval": 600,  # 产生阳光间隔(帧)
        "color": "accent_yellow",
    },
    "peashooter": {
        "name": "豌豆射手",
        "cost": 100,
        "health": 100,
        "shoot_interval": 90,
        "damage": 20,
        "color": "accent_green",
    },
    "snowpea": {
        "name": "寒冰射手",
        "cost": 175,
        "health": 100,
        "shoot_interval": 90,
        "damage": 20,
        "slow_duration": 180,
        "color": "accent_blue",
    },
    "wallnut": {
        "name": "坚果墙",
        "cost": 50,
        "health": 400,
        "color": (180, 150, 120),
    },
    "cherrybomb": {
        "name": "樱桃炸弹",
        "cost": 150,
        "health": 100,
        "explosion_delay": 60,
        "explosion_damage": 1800,
        "explosion_range": 1.5,  # 格子数
        "color": "accent_red",
    },
}

# 僵尸配置
ZOMBIE_CONFIG = {
    "normal": {
        "name": "普通僵尸",
        "health": 200,
        "speed": 0.5,
        "damage": 1,
        "level": 1,
    },
    "conehead": {
        "name": "路障僵尸",
        "health": 200,
        "armor_health": 170,
        "speed": 0.5,
        "damage": 1,
        "level": 2,
    },
    "buckethead": {
        "name": "铁桶僵尸",
        "health": 200,
        "armor_health": 450,
        "speed": 0.5,
        "damage": 1,
        "level": 3,
    },
    "football": {
        "name": "橄榄球僵尸",
        "health": 400,
        "armor_health": 600,
        "speed": 0.8,
        "damage": 2,
        "level": 4,
    },
    "newspaper": {
        "name": "读报僵尸",
        "health": 300,
        "armor_health": 200,
        "speed": 0.4,
        "damage": 2,
        "level": 2,
        "rage_speed": 0.9,
        "rage_damage": 3,
    },
    "dancer": {
        "name": "跳舞僵尸",
        "health": 200,
        "speed": 0.6,
        "damage": 1,
        "level": 2,
    },
}

# 波次配置
WAVE_CONFIG = {
    "total_waves": 5,
    "zombies_per_wave": 5,
    "initial_spawn_interval": 600,
    "spawn_interval_decrease": 50,
    "min_spawn_interval": 300,
    # 僵尸出现概率 (wave: {zombie_type: probability})
    "spawn_rates": {
        1: {"normal": 1.0},
        2: {"normal": 0.5, "conehead": 0.3, "newspaper": 0.2},
        3: {"normal": 0.3, "conehead": 0.25, "buckethead": 0.25, "newspaper": 0.1, "dancer": 0.1},
        4: {"normal": 0.2, "conehead": 0.2, "buckethead": 0.2, "newspaper": 0.15, "dancer": 0.15, "football": 0.1},
        5: {"normal": 0.1, "conehead": 0.15, "buckethead": 0.2, "newspaper": 0.15, "dancer": 0.15, "football": 0.25},
    },
}

# 阳光配置
SUN_CONFIG = {
    "initial_sun": 150,
    "sun_value": 25,
    "sky_sun_interval": 300,
    "sun_lifetime": 400,
    "sun_fall_speed": 2,
    "sun_radius": 22,
}

# 子弹配置
PROJECTILE_CONFIG = {
    "pea": {
        "speed": 8,
        "damage": 20,
        "radius": 8,
    },
    "snow_pea": {
        "speed": 8,
        "damage": 20,
        "radius": 8,
        "slow_duration": 180,
    },
}
