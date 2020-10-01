
import pygame
from pygame.sprite import Sprite
Image = 'ship.bmp'


class Ship(Sprite):
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始化位置"""
        super(Ship,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船并为其设置外接矩形边框
        # 加载飞船
        self.image = pygame.image.load(Image)
        # 将图像设置为矩形边框
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将飞船放在屏幕底部中央
        # x 飞船中心坐标x
        self.rect.centerx = self.screen_rect.centerx
        # y 飞船下边缘坐标y
        self.rect.bottom = self.screen_rect.bottom
        # 在飞船的属性center中存储小数
        self.center = float(self.rect.centerx)

        # 设置移动标志
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        """设置飞船居中"""
        self.center = self.screen_rect.centerx


    # 设置左右移动
    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # 更改坐标值
        self.rect.centerx = self.center

    # 根据要求绘制飞船
    def blitme(self):
        self.screen.blit(self.image, self.rect)
    