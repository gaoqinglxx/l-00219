"""
植物大战僵尸游戏 - 主程序入口
模块化重构版本
"""
import pygame
import sys
import math

# 初始化 Pygame
pygame.init()

# 导入配置和模块
from config import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, COLORS,
                   CARD_AREA_Y, CARD_AREA_HEIGHT, GRID_OFFSET_X, GRID_OFFSET_Y, GRID_SIZE)
from game_state import GameState
from ui import (Button, FeedbackMessage, draw_background, draw_top_panel, 
               draw_card_area, draw_game_over, get_color, get_font, CHINESE_FONTS, 
               draw_menu_overlay, draw_main_menu)
import logger

# 创建游戏窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("植物大战僵尸")
clock = pygame.time.Clock()

# 初始化字体
try:
    font = get_font(CHINESE_FONTS, 22)
    font_small = get_font(CHINESE_FONTS, 16)
    font_large = get_font(CHINESE_FONTS, 42)
except Exception as e:
    logger.log_warning(f"字体加载失败: {e}")
    font = pygame.font.Font(None, 22)
    font_small = pygame.font.Font(None, 16)
    font_large = pygame.font.Font(None, 42)

fonts = (font, font_small, font_large)

# 游戏状态枚举
class GameScene:
    MAIN_MENU = 0
    PLAYING = 1


def draw_card_icon(surface, x, y, idx, dim=False):
    """绘制植物卡片图标"""
    cx, cy = x + 45, y + 50
    
    if idx == 0:  # 向日葵
        c = (139 if not dim else 70, 90 if not dim else 45, 43 if not dim else 22)
        pygame.draw.circle(surface, c, (cx, cy), 10)
        for i in range(8):
            angle = i * math.pi / 4
            px, py = cx + math.cos(angle) * 14, cy + math.sin(angle) * 14
            color = get_color("accent_yellow") if not dim else (128, 100, 25)
            pygame.draw.circle(surface, color, (int(px), int(py)), 5)
        pygame.draw.rect(surface, get_color("dark_green") if not dim else (20, 60, 20), 
                        (cx - 2, cy + 10, 4, 12))
    elif idx == 1:  # 豌豆射手
        c = get_color("green") if not dim else (30, 90, 30)
        pygame.draw.circle(surface, c, (cx, cy), 12)
        pygame.draw.circle(surface, get_color("light_green") if not dim else (60, 110, 60), 
                          (cx - 3, cy - 4), 4)
        pygame.draw.ellipse(surface, get_color("dark_green") if not dim else (20, 60, 20), 
                           (cx + 6, cy - 4, 10, 8))
        pygame.draw.circle(surface, get_color("white") if not dim else get_color("gray"), 
                          (cx - 3, cy - 2), 4)
        pygame.draw.circle(surface, get_color("black"), (cx - 2, cy - 2), 2)
        pygame.draw.rect(surface, get_color("dark_green") if not dim else (20, 60, 20), 
                        (cx - 3, cy + 10, 6, 12))
    
    elif idx == 2:  # 寒冰射手
        c = get_color("accent_blue") if not dim else (50, 75, 128)
        pygame.draw.circle(surface, c, (cx, cy), 12)
        pygame.draw.circle(surface, (180, 220, 255) if not dim else (90, 110, 128), 
                          (cx - 3, cy - 4), 4)
        pygame.draw.ellipse(surface, (0, 80, 120) if not dim else (0, 40, 60), 
                           (cx + 6, cy - 4, 10, 8))
        pygame.draw.circle(surface, get_color("white") if not dim else get_color("gray"), 
                          (cx - 3, cy - 2), 4)
        pygame.draw.circle(surface, (0, 40, 80), (cx - 2, cy - 2), 2)
        pygame.draw.rect(surface, (0, 80, 120) if not dim else (0, 40, 60), 
                        (cx - 3, cy + 10, 6, 12))
    
    elif idx == 3:  # 坚果墙
        c = (200, 170, 130) if not dim else (100, 85, 65)
        d = (170, 140, 100) if not dim else (85, 70, 50)
        pygame.draw.ellipse(surface, c, (cx - 12, cy - 15, 24, 32))
        pygame.draw.ellipse(surface, d, (cx - 8, cy - 11, 16, 24))
        pygame.draw.circle(surface, get_color("white") if not dim else get_color("gray"), 
                          (cx - 4, cy - 4), 3)
        pygame.draw.circle(surface, get_color("white") if not dim else get_color("gray"), 
                          (cx + 4, cy - 4), 3)
        pygame.draw.circle(surface, get_color("black"), (cx - 3, cy - 4), 1)
        pygame.draw.circle(surface, get_color("black"), (cx + 5, cy - 4), 1)
    
    elif idx == 4:  # 樱桃炸弹
        c = get_color("accent_red") if not dim else (110, 40, 40)
        pygame.draw.circle(surface, c, (cx - 8, cy + 2), 10)
        pygame.draw.circle(surface, c, (cx + 8, cy + 2), 10)
        pygame.draw.circle(surface, (255, 120, 120) if not dim else (128, 60, 60), 
                          (cx - 11, cy - 3), 3)
        pygame.draw.circle(surface, (255, 120, 120) if not dim else (128, 60, 60), 
                          (cx + 5, cy - 3), 3)
        pygame.draw.line(surface, get_color("dark_green") if not dim else (20, 60, 20), 
                        (cx - 8, cy - 8), (cx, cy - 18), 2)
        pygame.draw.line(surface, get_color("dark_green") if not dim else (20, 60, 20), 
                        (cx + 8, cy - 8), (cx, cy - 18), 2)


def draw_plant_cards(surface, game_state, fonts):
    """绘制植物卡片"""
    font_small = fonts[1]
    
    for i, card in enumerate(game_state.plant_cards):
        x = 140 + i * 100
        y = CARD_AREA_Y + 10
        dim = game_state.sun_count < card["cost"]
        
        # 卡片背景
        bg_color = get_color("dark_card") if not dim else (30, 30, 40)
        pygame.draw.rect(surface, bg_color, (x, y, 90, 100), border_radius=8)
        
        # 选中边框
        if game_state.selected_index == i:
            pygame.draw.rect(surface, get_color("accent_yellow"), (x, y, 90, 100), 3, border_radius=8)
        else:
            pygame.draw.rect(surface, (60, 60, 80), (x, y, 90, 100), 1, border_radius=8)
        
        # 植物图标
        draw_card_icon(surface, x, y, i, dim)
        
        # 费用
        pygame.draw.rect(surface, (25, 25, 35), (x + 5, y + 78, 80, 18), border_radius=4)
        sun_color = get_color("accent_yellow") if not dim else (80, 65, 25)
        pygame.draw.circle(surface, sun_color, (x + 18, y + 87), 6)
        if font_small:
            cost_text = font_small.render(str(card["cost"]), True, 
                                         get_color("white") if not dim else get_color("gray"))
            surface.blit(cost_text, (x + 28, y + 80))


def draw_game(surface, game_state, feedback, fonts, restart_btn, menu_btn, menu_buttons):
    """绘制游戏画面"""
    draw_background(surface)
    
    # 绘制实体
    for plant in game_state.plants:
        plant.draw(surface)
    for proj in game_state.projectiles:
        proj.draw(surface)
    for zombie in game_state.zombies:
        zombie.draw(surface)
    for sun in game_state.suns:
        sun.draw(surface)
    
    # 绘制UI
    draw_top_panel(surface, game_state.sun_count, game_state.wave, 
                  game_state.total_waves, fonts)
    draw_card_area(surface, fonts)
    draw_plant_cards(surface, game_state, fonts)
    
    # 绘制菜单按钮
    menu_btn.draw(surface)
    
    # 选中植物跟随鼠标
    if game_state.selected_index >= 0 and not game_state.show_menu:
        pos = pygame.mouse.get_pos()
        s = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(s, (255, 255, 255, 80), (25, 25), 22)
        surface.blit(s, (pos[0] - 25, pos[1] - 25))
        draw_card_icon(surface, pos[0] - 45, pos[1] - 50, game_state.selected_index, False)
    
    # 反馈消息
    feedback.draw(surface)
    
    # 游戏结束/胜利
    if game_state.game_over or game_state.victory:
        draw_game_over(surface, fonts, restart_btn, game_state.victory)
    
    # 菜单覆盖层
    if game_state.show_menu:
        draw_menu_overlay(surface, menu_buttons, fonts[2])


def handle_click(pos, game_state, feedback, restart_btn, menu_btn, menu_buttons, running):
    """处理鼠标点击"""
    # 菜单逻辑
    if game_state.show_menu:
        btn_resume, btn_restart, btn_back_menu = menu_buttons
        if btn_resume.is_clicked(pos):
            game_state.show_menu = False
        elif btn_restart.is_clicked(pos):
            game_state.reset()
            game_state.show_menu = False
        elif btn_back_menu.is_clicked(pos):
            return "main_menu"  # 返回主菜单
        return True # 继续运行

    # 菜单按钮点击
    if menu_btn.is_clicked(pos):
        game_state.show_menu = True
        return True

    # 游戏结束时检查重新开始按钮
    if game_state.game_over or game_state.victory:
        if restart_btn.is_clicked(pos):
            game_state.reset()
        return True
    
    # 收集阳光
    if game_state.collect_sun(pos, feedback):
        return True
    
    # 选择植物卡片
    for i in range(len(game_state.plant_cards)):
        card_x = 140 + i * 100
        card_rect = pygame.Rect(card_x, CARD_AREA_Y + 10, 90, 100)
        if card_rect.collidepoint(pos):
            game_state.try_select_plant(i, feedback)
            return True
    
    # 放置植物
    if game_state.selected_plant_key:
        grid_x = (pos[0] - GRID_OFFSET_X) // GRID_SIZE
        grid_y = (pos[1] - GRID_OFFSET_Y) // GRID_SIZE
        game_state.try_place_plant(grid_x, grid_y, feedback)
    
    return True


def main():
    """主函数"""
    logger.log_game_start()
    
    try:
        game_state = GameState()
        feedback = FeedbackMessage()
        current_scene = GameScene.MAIN_MENU
        
        # 游戏内按钮
        restart_btn = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 40, 160, 50, "重新开始")
        menu_btn = Button(SCREEN_WIDTH - 80, 5, 70, 45, "菜单", "dark_gray")
        
        # 游戏内菜单按钮
        btn_resume = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 60, 160, 50, "继续游戏", "accent_green")
        btn_restart = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10, 160, 50, "重新开始", "accent_yellow")
        btn_back_menu = Button(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 80, 160, 50, "返回主菜单", "accent_red")
        menu_buttons = [btn_resume, btn_restart, btn_back_menu]
        
        # 主界面按钮
        main_btn_start = Button(SCREEN_WIDTH // 2 - 100, 200, 200, 55, "开始游戏", "accent_green")
        main_btn_exit = Button(SCREEN_WIDTH // 2 - 100, 280, 200, 55, "退出游戏", "accent_red")
        main_menu_buttons = [main_btn_start, main_btn_exit]
        
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键
                        if current_scene == GameScene.MAIN_MENU:
                            # 主界面点击处理
                            if main_btn_start.is_clicked(event.pos):
                                game_state.reset()
                                current_scene = GameScene.PLAYING
                            elif main_btn_exit.is_clicked(event.pos):
                                running = False
                        else:
                            # 游戏内点击处理
                            result = handle_click(event.pos, game_state, feedback, restart_btn, menu_btn, menu_buttons, running)
                            if result == "main_menu":
                                current_scene = GameScene.MAIN_MENU
                                game_state.show_menu = False
                            elif result == False:
                                running = False
                    elif event.button == 3 and current_scene == GameScene.PLAYING:  # 右键取消
                        game_state.selected_plant_key = None
                        game_state.selected_index = -1
                        feedback.add("取消选择", "gray", duration=45)
                elif event.type == pygame.KEYDOWN:
                    if current_scene == GameScene.PLAYING:
                        if event.key == pygame.K_p:
                            game_state.paused = not game_state.paused
                            feedback.add("暂停" if game_state.paused else "继续", "accent_yellow")
                        elif event.key == pygame.K_ESCAPE:
                            if game_state.show_menu:
                                game_state.show_menu = False
                            else:
                                game_state.selected_plant_key = None
                                game_state.selected_index = -1
                                game_state.show_menu = True
                    elif current_scene == GameScene.MAIN_MENU:
                        if event.key == pygame.K_RETURN:
                            game_state.reset()
                            current_scene = GameScene.PLAYING

            # 更新
            if current_scene == GameScene.MAIN_MENU:
                for btn in main_menu_buttons:
                    btn.update(mouse_pos)
            else:
                if not game_state.show_menu:
                    game_state.update()
                    feedback.update()
                
                if game_state.game_over or game_state.victory:
                    restart_btn.update(mouse_pos)
                
                menu_btn.update(mouse_pos)
                if game_state.show_menu:
                    for btn in menu_buttons:
                        btn.update(mouse_pos)
            
            # 绘制
            if current_scene == GameScene.MAIN_MENU:
                draw_main_menu(screen, main_menu_buttons, fonts)
            else:
                draw_game(screen, game_state, feedback, fonts, restart_btn, menu_btn, menu_buttons)
            
            pygame.display.flip()
            clock.tick(FPS)
        
    except Exception as e:
        logger.log_error("游戏运行错误", e)
        raise
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
