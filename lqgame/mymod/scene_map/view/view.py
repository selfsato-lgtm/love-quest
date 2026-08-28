import pygame
from ...data.app import U, W
from . import item, minimap, text

ui_w = W
ui_h = int(U * 3.25)

bg = pygame.Surface((ui_w, ui_h), pygame.SRCALPHA)
bg.fill((0, 0, 0, 128))

# 初期化
def init():
    minimap.init(ui_w, ui_h)    # ミニマップの初期化

# 全てを描画
def draw(screen: pygame.Surface):
    screen.blit(bg, (0, 0)) # 背景の描画
    text.draw(screen)       # テキストの描画
    minimap.draw(screen)    # ミニマップの描画
    item.draw(screen)       # アイテムの描画
