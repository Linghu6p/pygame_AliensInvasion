import time


class Settings():
    def __init__(self):
        """初始化游戏设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船数量设置
        self.ship_limit = 2

        # 子弹设置
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 220, 120, 150
        self.bullets_allowed = 20  # 每次只能发射20发

        # 外星人下降速度设置
        self.fleet_drop_speed = 10

        # 加快游戏节奏的速度
        self.speed_up_scale = 1.1

        # 外星人分数变化
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        # 外星人移动方向 1 为右
        self.fleet_direction = 1

        # 杀死一个得 50 分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度"""
        self.ship_speed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale
        self.alien_points = int(self.alien_points*self.score_scale)
