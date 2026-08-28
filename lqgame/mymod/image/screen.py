import pygame
from ..data.app import W, H, TITLE, IMAGE_ICON

buffer: pygame.Surface = pygame.Surface((W, H))

# ウィンドウの初期化
def init_win():
    # 開始画面サイズの計算と画面の作成
    d = pygame.display.get_desktop_sizes()[0]
    scale = min(d[0] * 0.8 // W, d[1] * 0.8 // H)   # 開始倍率
    size = (W * scale, H * scale)   # 開始画面サイズ
    pygame.display.set_mode(size, pygame.RESIZABLE) # 画面作成

    # ウィンドウの設定
    pygame.display.set_caption(TITLE)   # タイトルバー
    icon = pygame.image.load(IMAGE_ICON)
    pygame.display.set_icon(icon)   # アイコン

# バッファ取得
def get_buffer() -> pygame.Surface:
    return buffer

# 更新の前処理
def update_pre():
    pygame.display.update()     # 画面を更新

# 画面の消去
def clear():
    buffer.fill(pygame.Color(0, 0, 0))  # 画面を塗りつぶす

# 更新の後処理
def update_post():
    # 拡大率を計算して、バッファを拡大
    win = pygame.display.get_window_size()
    scale = min(win[0] / W, win[1] / H)
    dst = (W * scale, H * scale)
    scaled_buffer = pygame.transform.scale(buffer, dst)

    # オフセット位置を計算して描画
    offset = ((win[0] - dst[0]) / 2, (win[1] - dst[1]) / 2)
    screen = pygame.display.get_surface()
    screen.blit(scaled_buffer, offset)

    pygame.display.flip()       # 画面フリップ
