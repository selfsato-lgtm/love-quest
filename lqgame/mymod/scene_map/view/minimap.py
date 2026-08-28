import pygame
from ... import data

scale = 0
rect = pygame.Rect(0, 0, 0, 0)
image = pygame.Surface((0, 0))

# 初期化
def init(ui_w: int, ui_h: int):
    global scale, rect, image
    d = data.game.data

    # 描画位置とサイズの計算
    scale = (ui_h - 4) // d.map_h
    s = scale   # 1マスサイズと同等
    rect.w = s * d.map_w
    rect.h = s * d.map_h
    rect.y = int(ui_h - rect.h) // 2
    rect.x = ui_w - rect.w - rect.y

    # ミニマップの作成と描画
    image = pygame.Surface((rect.w, rect.h))
    for i, p in enumerate(d.data_map.map):
        x = i % d.map_w
        y = i // d.map_w
        pygame.draw.rect(image, data.map.COLS[p], (x * s, y * s, s, s))

# 描画
def draw(screen: pygame.Surface):
    # ミニマップの描画
    screen.blit(image, rect)

    # 主人公位置の描画
    d = data.game.data
    s = scale
    x = rect.x + (d.x - 1) * s
    y = rect.y + (d.y - 1) * s
    pygame.draw.rect(screen, (255, 255, 255), (x - 1, y - 1, s + 2, s + 2))
    pygame.draw.rect(screen, (255, 0, 0), (x, y, s, s))
