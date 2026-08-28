import pygame
from ... import data
from ...data.app import U, W, H
from ...image import font

# テキストの描画
def draw(screen: pygame.Surface):
    d = data.game.data

    # ステータスの描画
    x = U // 2
    y = U // 8
    text = f"Hero HP:{d.hp}/{d.hp_max} MP:{d.mp}/{d.mp_max}"
    font.draw_text(screen, x, y, text, is_frame=True)   # 1行目

    y += font.Size.M + 1
    text = f"LV:{d.level} EXP:{d.exp} AT:{d.at} DF:{d.df}"
    font.draw_text(screen, x, y, text, is_frame=True)   # 2行目

    y += font.Size.M + 1
    font.draw_text(screen, x, y, "M:Mute ESC:Quit", is_frame=True)  # 3行目

    # データ入出力のUIの描画
    x = W - int(U * 2.75)
    y = H - U
    font.draw_text(screen, x, y, "K:SAVE", is_frame=True)
