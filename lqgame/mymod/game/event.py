import pygame as pg
from . import audio

K_NONE  = "none"
K_LEFT  = "left"
K_RIGHT = "right"
K_UP    = "up"
K_DOWN  = "down"
K_SEL   = "select"
K_OPT   = "opt"

DRAG_DEAD_ZONE = 12   # この距離(px)未満の移動は「タップ」扱い

# ゲーム イベント
class GEvent:
    running: bool = True    # 実行状態フラグ
    key_down: str = K_NONE  # キー押下
    key_keep: str = K_NONE  # キー保持

# タッチ/マウス操作の状態(スマホ等でのドラッグ移動・タップ決定用)
_touch_start: tuple[float, float] | None = None
_touch_now: tuple[float, float] | None = None
_touch_active = False

def _drag_dir(start: tuple[float, float], now: tuple[float, float]) -> str:
    dx = now[0] - start[0]
    dy = now[1] - start[1]
    if abs(dx) < DRAG_DEAD_ZONE and abs(dy) < DRAG_DEAD_ZONE: return K_NONE
    if abs(dx) > abs(dy):
        return K_RIGHT if dx > 0 else K_LEFT
    return K_DOWN if dy > 0 else K_UP

# イベント処理
def exec() -> GEvent:
    global _touch_start, _touch_now, _touch_active
    e = GEvent()
    win_w, win_h = pg.display.get_window_size()

    for event in pg.event.get():
        if event.type == pg.QUIT: e.running = False # 終了

        if event.type == pg.KEYDOWN:
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

        # タッチ操作(スマホ/タブレット): ドラッグで移動、タップで決定
        elif event.type == pg.FINGERDOWN:
            _touch_start = _touch_now = (event.x * win_w, event.y * win_h)
            _touch_active = True
        elif event.type == pg.FINGERMOTION:
            if _touch_active:
                _touch_now = (event.x * win_w, event.y * win_h)
        elif event.type == pg.FINGERUP:
            if _touch_active and _touch_start and _touch_now:
                if _drag_dir(_touch_start, _touch_now) == K_NONE:
                    e.key_down = K_SEL   # ほとんど動かさず離した = タップ = 決定
            _touch_active = False
            _touch_start = _touch_now = None

        # マウス操作(PCブラウザでの動作確認用、タッチと同じ扱い)
        elif event.type == pg.MOUSEBUTTONDOWN:
            _touch_start = _touch_now = event.pos
            _touch_active = True
        elif event.type == pg.MOUSEMOTION:
            if _touch_active:
                _touch_now = event.pos
        elif event.type == pg.MOUSEBUTTONUP:
            if _touch_active and _touch_start and _touch_now:
                if _drag_dir(_touch_start, _touch_now) == K_NONE:
                    e.key_down = K_SEL
            _touch_active = False
            _touch_start = _touch_now = None

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

    # キーボード入力が無ければ、ドラッグ中の方向を移動として反映
    if r == K_NONE and _touch_active and _touch_start and _touch_now:
        r = _drag_dir(_touch_start, _touch_now)

    e.key_keep = r
    return e
