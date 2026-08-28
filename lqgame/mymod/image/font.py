import pygame
from .. import data

fonts: dict[int, pygame.font.Font] = {}
BASE = 12
class Size:
    M  = BASE * 1
    L  = BASE * 2
    L2 = BASE * 3
    L3 = BASE * 4
    L4 = BASE * 5
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)

# 初期化（フォントを読み込み、サイズごとに初期化する）
def init():
    for k, v in Size.__dict__.items():
        if k.startswith("__"): continue
        fonts[v] = pygame.font.Font(data.app.FONT, v)

# 指定文字列と色のSurfaceを得る
def get_surface(text: str, id: int, color: pygame.Color) -> pygame.Surface:
    return fonts[id].render(text, False, color)

# 文字列描画
def draw_text(screen: pygame.Surface, x: int, y: int, text: str,
        id: int = Size.M, color: pygame.Color = WHITE,
        is_center: bool = False, is_frame: bool = False):
    surface = get_surface(text, id, color)

    if is_center == True: x -= surface.get_width() // 2 # 中央描画

    if is_frame == True:    # 枠付き描画
        col2 = BLACK if color == WHITE else WHITE   # 色逆転
        surface2 = get_surface(text, id, col2)
        for i in range(9):  # 周囲1マス描画
            mx = - 1 + i % 3
            my = - 1 + i // 3
            screen.blit(surface2, (x + mx, y + my))

    screen.blit(surface, (x, y))    # 描画
