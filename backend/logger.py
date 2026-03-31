"""
日志模块 - 游戏状态日志与错误处理
"""
import logging
import sys
from datetime import datetime

# 配置日志格式
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
DATE_FORMAT = "%H:%M:%S"

# 创建logger
logger = logging.getLogger("PVZ")
logger.setLevel(logging.DEBUG)

# 控制台处理器
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
logger.addHandler(console_handler)

# 文件处理器
try:
    file_handler = logging.FileHandler("pvz_game.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
    logger.addHandler(file_handler)
except Exception as e:
    logger.warning(f"无法创建日志文件: {e}")


def log_game_start():
    logger.info("=" * 50)
    logger.info("游戏启动")
    logger.info("=" * 50)


def log_game_reset():
    logger.info("游戏重置")


def log_plant_placed(plant_name: str, row: int, col: int, cost: int, remaining_sun: int):
    logger.info(f"放置植物: {plant_name} 位置({row},{col}) 花费{cost} 剩余阳光{remaining_sun}")


def log_plant_destroyed(plant_name: str, row: int, col: int):
    logger.info(f"植物被摧毁: {plant_name} 位置({row},{col})")


def log_zombie_spawned(zombie_name: str, row: int, wave: int):
    logger.debug(f"僵尸出现: {zombie_name} 行{row} 波次{wave}")


def log_zombie_killed(zombie_name: str):
    logger.debug(f"僵尸被消灭: {zombie_name}")


def log_wave_start(wave: int, total: int):
    logger.info(f"波次开始: {wave}/{total}")


def log_wave_complete(wave: int):
    logger.info(f"波次完成: {wave}")


def log_game_over():
    logger.info("游戏结束 - 僵尸入侵成功")


def log_victory():
    logger.info("游戏胜利!")


def log_sun_collected(value: int, total: int):
    logger.debug(f"收集阳光: +{value} 总计{total}")


def log_error(message: str, exception: Exception = None):
    if exception:
        logger.error(f"{message}: {exception}")
    else:
        logger.error(message)


def log_warning(message: str):
    logger.warning(message)
