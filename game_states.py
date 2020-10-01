class GameStates():
    """ 统计游戏内的信息"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        # 使得游戏一开始处于非活跃状态
        self.game_active = False

        # 不会改变最高得分
        self.high_score = 0

        # 游戏等级
        self.level = 1

    def reset_stats(self):
        """初始化游戏信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
