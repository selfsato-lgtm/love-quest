import pygame
from ... import data
from ...image.font import draw_text
from ...data.app import U, W, H

# 全て描画
def draw(screen: pygame.Surface, menu: data.action.Menu):
    draw_frame(screen)  # 枠線描画
    draw_status_enemy(screen)   # 敵ステータス描画
    draw_status_my(screen)      # 自ステータス描画
    draw_menu(screen, menu)     # メニュー描画

# 枠線描画
def draw_frame(screen: pygame.Surface):
    rect1 = pygame.Rect(U, U, W - U * 2, U * 8)
    rect2 = pygame.Rect(U, U * 9.25, W - U * 2, H - U * 10.25)
    pygame.draw.rect(screen, (255, 255, 255), rect1, 2) # 枠線1
    pygame.draw.rect(screen, (255, 255, 255), rect2, 2) # 枠線2

# 敵ステータス描画
def draw_status_enemy(screen: pygame.Surface):
    x = W // 2
    y = int(U * 1.25)
    e = data.enemy.enemy_now
    text = f"{e.name}  HP: {e.hp} / {e.hp_max}"
    draw_text(screen, x, y, text, is_center=True)

# 自ステータス描画
def draw_status_my(screen: pygame.Surface):
    x = int(U * 1.5)
    y = int(U * 9.75)
    d = data.game.data
    texts = [f"Hero   LV: {d.level}",    f"HP: {d.hp} / {d.hp_max}",
             f"MP: {d.mp} / {d.mp_max}", f"AT: {d.at} DF: {d.df}"]

    # 文字描画
    for i, text in enumerate(texts):
        draw_text(screen, x, y + i * U, text)

# メニュー描画
def draw_menu(screen: pygame.Surface, menu: data.action.Menu):
    x = int(U * 7.5)
    y = int(U * 9.75)
    w = int(U * 11.5)
    rect = pygame.Rect(x - U // 4, y - U // 16, w, U)

    # メニュー描画
    for i, text in enumerate(menu.texts):
        if i == menu.sel:   # 選択メニュー描画
            rect.y += i * U
            pygame.draw.rect(screen, (64, 64, 64), rect)
        draw_text(screen, x, y + i * U, f"> {text}")
