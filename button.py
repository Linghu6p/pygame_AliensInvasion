import pygame.font
"""pygame.font 可以将文字渲染到屏幕上"""

import pygame


class Button():
    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置开始游戏按钮
        self.width, self.height = 200, 50
        self.button_color = (0, 225, 0)
        self.text_color = (225, 225, 225)
        # 设置字体
        self.font = pygame.font.SysFont(None, 48)

        # Rect 设置矩形 和制作子弹方法一样
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 创建按钮标签
        self.prep_msg(msg)

    def prep_msg(self, msg):
        # 调用 font.render() 可以将文字转换为图像 True表示有无锯齿
        self.msg_image = self.font.render(
            msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        # 将文字放在矩形框中央
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制按钮用颜色填充
        self.screen.fill(self.button_color,self.rect)
        # 绘制文本 
        self.screen.blit(self.msg_image,self.msg_image_rect)

