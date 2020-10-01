import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    def __init__(self, ai_settings, screen, stats):
        # 得分属性初始化
        self.screen = screen
        self.stats = stats
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()

        # 字体设置
        self.text_color = (30, 30, 30)

        self.font = pygame.font.SysFont(None, 48)
        # 准备初始得分图像和最高得分图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = 10+ship_number*ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def prep_level(self):
        self.level_image = self.font.render(
            str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_score(self):
        # 圆整化 即让分数为 10（100 100）的倍数(与round有关)  round 第二个时参确定小数位数  负数代表最近的10 100 1000整数倍数
        rounded_score = int(round(self.stats.score, -1))
        # 字符串格式设置指令 意思是将数字转化为字符串时在里面插入逗号
        score_str = "{:,}".format(rounded_score)
        # render 表示图像有无锯齿
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.ai_settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def prep_high_score(self):
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(
            high_score_str, True, self.text_color, self.ai_settings.bg_color)

        # 设置最高得分位置
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def show_score(self):
        # 绘制文本 可以理解为用 image去填充矩形框
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
