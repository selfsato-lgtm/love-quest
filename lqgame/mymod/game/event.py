import pygame as pg
from . import audio

K_NONE  = "none"
K_LEFT  = "left"
K_RIGHT = "right"
K_UP    = "up"
K_DOWN  = "down"
K_SEL   = "select"
K_OPT   = "opt"

# ゲーム イベント
class GEvent:
    running: bool = True    # 実行状態フラグ
    key_down: str = K_NONE  # キー押下
    key_keep: str = K_NONE  # キー保持

# イベント処理
def exec() -> GEvent:
    e = GEvent()

    for event in pg.event.get():
        if event.type == pg.QUIT: e.running = False # 終了
        if event.type != pg.KEYDOWN: continue   # キー押下でない

        # キー押下
        k = event.key
        r = K_NONE
        if k == pg.K_LEFT:   r = K_LEFT     # 左
        if k == pg.K_RIGHT:  r = K_RIGHT    # 右
        if k == pg.K_UP:     r = K_UP       # 上
        if k == pg.K_DOWN:   r = K_DOWN     # 下
        if k == pg.K_a:      r = K_LEFT     # 左
        if k == pg.K_d:      r = K_RIGHT    # 右
        if k == pg.K_w:      r = K_UP       # 上
        if k == pg.K_s:      r = K_DOWN     # 下
        if k == pg.K_SPACE:  r = K_SEL      # 選択
        if k == pg.K_RETURN: r = K_SEL      # 選択
        if k == pg.K_k:      r = K_OPT      # オプション
        if k == pg.K_m:      audio.toggle_mute()  # ミュート切替
        if k == pg.K_ESCAPE: e.running = False     # 終了
        e.key_down = r

    # キー保持
    k = pg.key.get_pressed()
    r = K_NONE
    if k[pg.K_LEFT]:   r = K_LEFT   # 左
    if k[pg.K_RIGHT]:  r = K_RIGHT  # 右
    if k[pg.K_UP]:     r = K_UP     # 上
    if k[pg.K_DOWN]:   r = K_DOWN   # 下
    if k[pg.K_a]:      r = K_LEFT   # 左
    if k[pg.K_d]:      r = K_RIGHT  # 右
    if k[pg.K_w]:      r = K_UP     # 上
    if k[pg.K_s]:      r = K_DOWN   # 下
    if k[pg.K_SPACE]:  r = K_SEL    # 選択
    if k[pg.K_RETURN]: r = K_SEL    # 選択
    if k[pg.K_k]:      r = K_OPT    # オプション
    e.key_keep = r

    return e
