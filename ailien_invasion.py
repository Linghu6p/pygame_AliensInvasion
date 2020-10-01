import sys
import pygame
from ship import Ship
from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from alien import Alien
from game_states import GameStates
from button import Button
from scoreboard import Scoreboard


def run_game():
    # 初始屏幕设置 宽度 高度 背景
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    # 游戏名字 外星人入侵
    pygame.display.set_caption("Alien Invasion")

    # 创建开始按钮
    play_button = Button(ai_settings, screen, "Play")

    # 统计游戏信息的实例
    stats = GameStates(ai_settings)

    # 建立一艘飞船
    ship = Ship(ai_settings, screen)

    # 创建子弹
    bullets = Group()

    # 建立外星人
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # 创建记分牌
    sb = Scoreboard(ai_settings, screen, stats)

    # 开始游戏循环
    while 1:
        # 监听键盘和鼠标 见引用库
        gf.check_events(ai_settings, screen, stats, sb, play_button,
                        ship, aliens, bullets)

        if stats.game_active:
            # 设置飞船左右移动
            ship.update()
            # 设置子弹
            gf.update_bullets(ai_settings,  screen, stats,
                              sb, ship, aliens, bullets)
            # 外星人移动
            gf.update_aliens(ai_settings, screen, stats,
                             sb, ship, aliens, bullets)

        # 设置屏幕内的信息
        gf.update_screen(ai_settings, screen, stats, sb, ship,
                         aliens, bullets, play_button)


run_game()
