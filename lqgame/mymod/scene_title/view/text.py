import pygame
from ...data.app import U, W, H
from ...image import font

# 文字の設定
titles = (
    ("LOVEQUEST",               1,  font.Size.L4),
    ("PRESS SPACE KEY",         7,  font.Size.L),
    ("Move: W A S D, ↑←↓→", 10, font.Size.M),
    ("Select: Space, Enter",    11, font.Size.M),
    ("Mute: M key",             12, font.Size.M),
    ("Quit: ESC key",           13, font.Size.M),
    ("(c)2024 Masakazu Yanai",  15, font.Size.M)
)

# テキストの描画
def draw(screen: pygame.Surface):
    # タイトルの文字列の描画
    x = W // 2
    for i in titles:
        y = U * i[1]
        font.draw_text(screen, x, y, i[0], i[2], is_center=True)

    # データ入出力のUIの描画
    x = W - int(U * 2.75)
    y = H - U
    font.draw_text(screen, x, y, "K:LOAD")
