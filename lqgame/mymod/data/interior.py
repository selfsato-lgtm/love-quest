from dataclasses import dataclass
from . import map as map_mod

# 建物内マップのサイズ(種別ごと。画面(20x15マス)を程よく満たす広さにする)
SIZES = {
    map_mod.TOWN:   (19, 13),   # 街 広場
    map_mod.CASTLE: (17, 13),   # 魔王城 謁見の間
    map_mod.CAVE:   (15, 11),   # 洞窟
}

@dataclass
class NPC:
    x: int
    y: int
    img_nums: list[int]
    text: str

def build(kind: int) -> tuple[map_mod.Map, list[NPC]]:
    """街/城/洞窟の内部マップを生成する。外周は壁、中は床、下端中央が出口。
    街には宿(ベッド)とNPCを配置する。洞窟は岩を点在させ通路っぽい見た目にする"""
    w, h = SIZES.get(kind, (13, 10))
    m = [map_mod.FLOOR] * (w * h)

    for x in range(w):
        m[x] = map_mod.WALL              # 上端
        m[x + (h - 1) * w] = map_mod.WALL  # 下端
    for y in range(h):
        m[y * w] = map_mod.WALL          # 左端
        m[w - 1 + y * w] = map_mod.WALL  # 右端

    npcs: list[NPC] = []

    if kind == map_mod.CASTLE:
        # 玉座の間っぽく、左右対称の柱を並べる
        for y in range(2, h - 2, 2):
            m[2 + y * w] = map_mod.WALL
            m[w - 3 + y * w] = map_mod.WALL

    if kind == map_mod.CAVE:
        # 岩をランダムに点在させ、洞窟らしい通路にする
        from random import seed, randrange
        seed(kind * 7919 + w * h)
        for _ in range((w * h) // 8):
            x = randrange(2, w - 2)
            y = randrange(2, h - 2)
            m[x + y * w] = map_mod.WALL

    if kind == map_mod.TOWN:
        # 宿(左上にベッドを設置)
        bed_x, bed_y = 2, 2
        m[bed_x + bed_y * w] = map_mod.BED

        # NPC配置(広場中央付近に横並び)
        base_x = w // 2 - 2
        base_y = h // 2
        specs = [
            ([2, 3], "妖精\n「この街に\nようこそ！」"),
            ([6, 7], "シスター\n「宿で休んで\nいってね」"),
            ([8, 9], "姫\n「気になる子は\n見つかった？」"),
        ]
        for i, (img_nums, text) in enumerate(specs):
            npcs.append(NPC(base_x + i * 2, base_y, img_nums, text))

    exit_x = w // 2
    m[exit_x + (h - 1) * w] = map_mod.EXIT  # 出口(下端中央、通行可能を保証)
    m[exit_x + (h - 2) * w] = map_mod.FLOOR

    return map_mod.Map(w, h, m, []), npcs
