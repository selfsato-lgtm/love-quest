from random import seed, randrange
from dataclasses import dataclass

SEED = None     # ランダムのシード値（None or int）
PLAIN    = 0
FOLEST   = 1
MOUNTAIN = 2
WATER    = 3
TOWN     = 4
CASTLE   = 5
CAVE     = 6    # 洞窟入口(屋外マップ上に配置される)
WALL     = 7    # 建物内の壁(通行不可、屋外マップには配置しない)
FLOOR    = 8    # 建物内の床(通行可、屋外マップには配置しない)
EXIT     = 9    # 建物の出口(踏むと屋外マップへ戻る、屋外マップには配置しない)
BED      = 10   # 宿屋のベッド(踏むとHP/MP全回復、街の建物内にのみ配置)

COLS = [    # ミニ マップ用色配列
    (152, 232,   0),    # 平地
    ( 56, 104,   0),    # 森
    (192, 112,   0),    # 山
    ( 80, 128, 255),    # 水
    (232, 208,  32),    # 街
    (144,  64, 240),    # 魔王城
    ( 96,  88,  80),    # 洞窟
    (120, 120, 128),    # 壁
    (196, 164, 116),    # 床
    (150,  96,  52),    # 出口
    (232, 232, 240),    # ベッド
]

INTERIOR_KINDS = (TOWN, CASTLE, CAVE)   # 建物内に入れる土地種別
BLOCKED = (WATER, WALL)                 # 通行不可の土地種別

@dataclass
class Map:
    w: int
    h: int
    map: list[int]
    towns: list[list[int]]

    # 初期化
    @classmethod
    def from_wh(cls, w: int, h: int) -> "Map":
        res = Map(w, h, [], [])
        res.map = [PLAIN] * h * w
        return res

    # マップ生成
    def gen(self, start_x: int, start_y: int):
        seed(SEED)
        w, h, m = self.w, self.h, self.map

        # 水
        for i in range(int(w * 1.5)):
            x = randrange(w)
            y = randrange(h)
            for j in range(3):
                r = (j % 2) + 1
                x2 = x + randrange(-r, r, 1)
                y2 = y + randrange(-r, r, 1)
                x2 = (x2 + w) % w
                y2 = (y2 + h) % h
                m[x2 + y2 * w] = WATER

        # 開始位置（周囲の水を消す）
        for i in range(9):
            x = start_x - 1 + i % 3
            y = start_y - 1 + i // 3
            m[x + y * w] = PLAIN

        # 山と森
        for i in range(w):
            x = randrange(w)
            y = randrange(h)
            for j in range(24):
                r = (j % 3) + 1
                x2 = x + randrange(-r, r, 1)
                y2 = y + randrange(-r, r, 1)
                x2 = (x2 + w) % w
                y2 = (y2 + h) % h
                if j < 16:
                    m[x2 + y2 * w] = FOLEST
                else:
                    m[x2 + y2 * w] = MOUNTAIN

        # 街と城
        step = 5
        area_w = w // (step * 3)
        area_h = h // (step * 3)
        for i in range(9):
            x = i % 3
            y = i // 3
            x2 = (x * step + 1) * area_w + randrange(area_w * 3)
            y2 = (y * step + 1) * area_h + randrange(area_h * 3)
            if i == 4:
                m[x2 + y2 * w] = CASTLE
            else:
                m[x2 + y2 * w] = TOWN
                self.towns.append([x2, y2])

        # 洞窟(山地の中からランダムに選んで配置)
        mountains = [i for i, v in enumerate(m) if v == MOUNTAIN]
        for _ in range(min(3, len(mountains))):
            i = mountains.pop(randrange(len(mountains)))
            m[i] = CAVE
