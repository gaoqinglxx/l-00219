"""
游戏状态管理模块
"""
import random
from config import (WAVE_CONFIG, SUN_CONFIG, PLANT_CONFIG, 
                   GRID_OFFSET_X, GRID_OFFSET_Y, GRID_SIZE, ROWS, COLS,
                   SCREEN_WIDTH, CARD_AREA_Y)
from entities import Sun, Sunflower, Peashooter, SnowPea, WallNut, CherryBomb
from entities import Zombie, ConeheadZombie, BucketheadZombie, FootballZombie, NewspaperZombie, DancerZombie
import logger


# 植物类映射
PLANT_CLASSES = {
    "sunflower": Sunflower,
    "peashooter": Peashooter,
    "snowpea": SnowPea,
    "wallnut": WallNut,
    "cherrybomb": CherryBomb,
}

# 僵尸类映射
ZOMBIE_CLASSES = {
    "normal": Zombie,
    "conehead": ConeheadZombie,
    "buckethead": BucketheadZombie,
    "football": FootballZombie,
    "newspaper": NewspaperZombie,
    "dancer": DancerZombie,
}


class GameState:
    """游戏状态管理"""
    def __init__(self):
        self.reset()
        
    def reset(self):
        """重置游戏状态"""
        self.plants = []
        self.zombies = []
        self.projectiles = []
        self.suns = []
        self.sun_count = SUN_CONFIG["initial_sun"]
        self.selected_plant_key = None
        self.selected_index = -1
        
        self.wave = 1
        self.zombie_spawn_timer = 0
        self.zombie_spawn_interval = WAVE_CONFIG["initial_spawn_interval"]
        self.zombies_spawned = 0
        self.zombies_per_wave = WAVE_CONFIG["zombies_per_wave"]
        self.total_waves = WAVE_CONFIG["total_waves"]
        
        self.game_over = False
        self.victory = False
        self.paused = False
        self.show_menu = False
        
        self.sky_sun_timer = 0
        self.sky_sun_interval = SUN_CONFIG["sky_sun_interval"]
        
        self.grid = [[None for _ in range(COLS)] for _ in range(ROWS)]
        
        # 植物卡片配置
        self.plant_cards = []
        for key, config in PLANT_CONFIG.items():
            self.plant_cards.append({
                "key": key,
                "name": config["name"],
                "cost": config["cost"],
                "color": config["color"],
            })
        
        logger.log_game_reset()
    
    def get_spawn_rates(self):
        """获取当前波次的僵尸生成概率"""
        return WAVE_CONFIG["spawn_rates"].get(self.wave, {"normal": 1.0})
    
    def spawn_zombie(self):
        """生成僵尸"""
        row = random.randint(0, ROWS - 1)
        rates = self.get_spawn_rates()
        
        rand = random.random()
        cumulative = 0
        zombie_type = "normal"
        
        for ztype, prob in rates.items():
            cumulative += prob
            if rand <= cumulative:
                zombie_type = ztype
                break
        
        zombie_class = ZOMBIE_CLASSES.get(zombie_type, Zombie)
        zombie = zombie_class(row)
        self.zombies.append(zombie)
        self.zombies_spawned += 1
        logger.log_zombie_spawned(zombie.name, row, self.wave)

    def try_place_plant(self, grid_x, grid_y, feedback):
        """尝试放置植物，返回是否成功"""
        if self.selected_plant_key is None:
            return False
        
        if not (0 <= grid_x < COLS and 0 <= grid_y < ROWS):
            feedback.add("无效位置!", "accent_red")
            return False
        
        if self.grid[grid_y][grid_x] is not None:
            feedback.add("该位置已有植物!", "accent_red")
            return False
        
        card = self.plant_cards[self.selected_index]
        cost = card["cost"]
        
        if self.sun_count < cost:
            feedback.add(f"阳光不足! 需要{cost}", "accent_red")
            return False
        
        # 创建植物
        plant_class = PLANT_CLASSES.get(self.selected_plant_key)
        if plant_class:
            plant = plant_class(grid_y, grid_x)
            self.plants.append(plant)
            self.grid[grid_y][grid_x] = plant
            self.sun_count -= cost
            
            logger.log_plant_placed(plant.name, grid_y, grid_x, cost, self.sun_count)
            feedback.add(f"放置{plant.name}!", "accent_green")
            
            self.selected_plant_key = None
            self.selected_index = -1
            return True
        
        return False
    
    def try_select_plant(self, index, feedback):
        """尝试选择植物卡片"""
        if 0 <= index < len(self.plant_cards):
            card = self.plant_cards[index]
            if self.sun_count >= card["cost"]:
                self.selected_plant_key = card["key"]
                self.selected_index = index
                feedback.add(f"选择{card['name']}", "accent_yellow", duration=60)
                return True
            else:
                feedback.add(f"阳光不足! 需要{card['cost']}", "accent_red")
        return False
    
    def collect_sun(self, pos, feedback):
        """收集阳光"""
        for sun in self.suns:
            if sun.is_clicked(pos) and not sun.collected:
                sun.collected = True
                feedback.add(f"+{sun.value}", "accent_yellow", duration=45, x=pos[0], y=pos[1])
                return True
        return False
    
    def update(self):
        """更新游戏状态"""
        if self.game_over or self.victory or self.paused:
            return
        
        # 天空阳光
        self.sky_sun_timer += 1
        if self.sky_sun_timer >= self.sky_sun_interval:
            self.sky_sun_timer = 0
            empty_cells = []
            for row in range(ROWS):
                for col in range(COLS):
                    if self.grid[row][col] is None:
                        empty_cells.append((row, col))
            
            if empty_cells:
                row, col = random.choice(empty_cells)
                x = GRID_OFFSET_X + col * GRID_SIZE + GRID_SIZE // 2
                y = GRID_OFFSET_Y + row * GRID_SIZE + GRID_SIZE // 2
                self.suns.append(Sun(x, y, from_sky=True, row=row, col=col))
        
        # 更新阳光
        for sun in self.suns[:]:
            collected = sun.update()
            if collected:
                self.sun_count += collected
                logger.log_sun_collected(collected, self.sun_count)
            
            if sun.reached_target and not sun.collected and sun.row is not None and sun.col is not None:
                if 0 <= sun.row < ROWS and 0 <= sun.col < COLS:
                    if self.grid[sun.row][sun.col] is not None:
                        sun.collected = True
            
            if not sun.alive:
                self.suns.remove(sun)
        
        # 生成僵尸
        self.zombie_spawn_timer += 1
        if self.zombie_spawn_timer >= self.zombie_spawn_interval:
            total_this_wave = self.zombies_per_wave * self.wave
            if self.zombies_spawned < total_this_wave:
                self.spawn_zombie()
                self.zombie_spawn_timer = 0
        
        # 更新植物
        for plant in self.plants[:]:
            plant.update(self.zombies, self.projectiles, self.suns)
            if not plant.alive:
                self.grid[plant.row][plant.col] = None
                self.plants.remove(plant)
                logger.log_plant_destroyed(plant.name, plant.row, plant.col)
        
        # 更新子弹
        for proj in self.projectiles[:]:
            proj.update(self.zombies)
            if not proj.alive:
                self.projectiles.remove(proj)
        
        # 更新僵尸
        for zombie in self.zombies[:]:
            zombie.update(self.plants)
            if not zombie.alive:
                self.zombies.remove(zombie)
                logger.log_zombie_killed(zombie.name)
            elif zombie.x < GRID_OFFSET_X - 40:
                self.game_over = True
                logger.log_game_over()
        
        # 检查波次完成
        total_this_wave = self.zombies_per_wave * self.wave
        if self.zombies_spawned >= total_this_wave and len(self.zombies) == 0:
            if self.wave >= self.total_waves:
                self.victory = True
                logger.log_victory()
            else:
                logger.log_wave_complete(self.wave)
                self.wave += 1
                self.zombies_spawned = 0
                decrease = WAVE_CONFIG["spawn_interval_decrease"]
                min_interval = WAVE_CONFIG["min_spawn_interval"]
                self.zombie_spawn_interval = max(min_interval, 
                                                 self.zombie_spawn_interval - decrease)
                logger.log_wave_start(self.wave, self.total_waves)
