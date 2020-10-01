import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def change_fleet_direction(ai_settings, aliens):
    """改变外星人方向 整体下移"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def get_number_aliens_x(ai_settigs, alien_width):
    """计算每行有多少外星人"""
    available_space_x = ai_settigs.screen_width - 2*alien_width
    number_aliens_x = int(available_space_x/(alien_width*2))
    return number_aliens_x


def get_number_rows(ai_settigs, ship_height, alien_height):
    """计算还能有多少行"""
    available_space_y = (ai_settigs.screen_height-(3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


# 创建外星人
def create_alien(ai_settigs, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settigs, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建一群外星人"""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(
        ai_settings, ship.rect.height, alien.rect.height)
    # 创建第一行外星人
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_high_score(stats, sb):
    if stats.score >= stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查外星人有无到达底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 子弹碰撞 groupcollide 用于删除碰撞的东西 True代表消失
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        # 当外星人都打完之后 刷新界面
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """响应松开按键"""
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """响应按键和鼠标事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            """响应鼠标，只要点击就返回，下面便是返回一个坐标值"""
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb,
                              play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    # collidepoint 检查是否在某个位置
    button_cliked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_cliked and not stats.game_active:
        # 隐藏光标 True就是显示
        pygame.mouse.set_visible(False)

        # 重置游戏
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        ai_settings.initialize_dynamic_settings()

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 创建外星人 让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)  # add在这里是将子弹存入编组bullets中


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """更新屏幕图像，并切换到新屏幕"""
    # 设置背景颜色
    screen.fill(ai_settings.bg_color)
    # 设置飞船
    ship.blitme()
    # 绘制外星人中的每一个元素 
    aliens.draw(screen)
    # 绘制子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # 显示得分
    sb.show_score()
    # 非活跃状态 显示 play
    if not stats.game_active:
        play_button.draw_button()
    # 让上面绘制的东西可见
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 设置子弹
    bullets.update()
    # 删除屏幕外的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(
        ai_settings, screen, stats, sb, ship, aliens, bullets)


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 检验外星人是否在边缘
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检验碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)
