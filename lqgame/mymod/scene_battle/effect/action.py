import math
from pygame import Color, draw, Rect
from . import manage    # 型ヒント用

# 斬撃
def draw_sword(args: "manage.Args", rect: Rect, color: Color):
    x, y, w, h = rect
    x1 = w * 0.1; x2 = w * 0.45; x3 = w * 0.9; x4 = w * 0.55
    y1 = 0;       y2 = h * 0.55; y3 = h;       y4 = h * 0.45
    if args.rate > 0.5:
        x1 = w * 0.9; x2 = w * 0.45; x3 = w * 0.1; x4 = w * 0.55
        y1 = 0;       y2 = h * 0.45; y3 = h;       y4 = h * 0.55
    points = [(x + x1, y + y1), (x + x2, y + y2),
              (x + x3, y + y3), (x + x4, y + y4)]
    draw.polygon(args.screen, color, points)

# 魔法
def draw_magic(args: "manage.Args", rect: Rect, color: Color):
    x, y, w, h = rect
    cx = x + w // 2     # 中心X
    cy = y + h // 2     # 中心Y
    r_max = math.sqrt(w * w + h * h) // 2   # 半径最大
    c_max = 24  # 円数最大
    c_now = min(c_max, int(args.rate * c_max + 0.5))    # 円数現在
    line_w = int(r_max / c_max / 2)     # 線幅
    for i in range(c_now):
        r = r_max * i / (c_max - 1)     # 半径
        draw.circle(args.screen, color, (cx, cy), r, line_w)

# 回復
def draw_heal(args: "manage.Args", rect: Rect, color: Color):
    x, y, w, h = rect
    dx = x + w / 2 * (1 - args.rate)
    dw = w * args.rate
    draw.rect(args.screen, color, (dx, y, dw, h))

# 打撃
def draw_hit(args: "manage.Args", rect: Rect, color: Color):
    x, y, w, h = rect
    n = args.time // 60
    cx = x + w * 0.2 + w * 0.6 * (n * 11 % 19 / 19)
    cy = y + h * 0.2 + h * 0.6 * (n * 11 % 17 / 17)
    r = min(w, h) * (0.2 + 0.2 * (n * 11 % 13 / 13))
    draw.circle(args.screen, color, (cx, cy), r)
