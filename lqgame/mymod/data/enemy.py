from dataclasses import dataclass, field
from .action import SWORD, ARROW, WIND, DEATH
from .map import PLAIN, FOLEST, MOUNTAIN, CASTLE

# 敵
@dataclass
class Enemy:
    name: str   # 名前
    rate: int   # 出現頻度 1/rate
    land: int   # 出現土地
    img_nums: list[int] # 画像参照位置のリスト
    hp_max: int # 最大HP
    at: int     # 攻撃力
    df: int     # 防御力
    action: str # 行動
    is_last: bool = False   # 最終ボス boolean
    hp: int = field(init = False)   # HP

    def __post_init__(self):
        self.hp = self.hp_max   # HP

# img_numsはbuild_chara_sheet.pyのCHARA_FILES順(行1から2チップずつ)と対応
ENEMIES = [    # 出現頻度 出現土地  画像参照    HP  攻撃 防御 攻撃種 ボス
    # PLAIN(平地) 弱め・遭遇率高め
    Enemy("妖精",     14, PLAIN,    [2, 3],    40, 16,  5, ARROW),
    Enemy("牧師",     13, PLAIN,    [4, 5],    45, 15,  7, SWORD),
    Enemy("シスター", 13, PLAIN,    [6, 7],    45, 14,  8, SWORD),
    Enemy("姫",       12, PLAIN,    [8, 9],    50, 18,  6, ARROW),
    Enemy("占い師",   12, PLAIN,    [10, 11],  50, 17,  8, WIND),

    # FOLEST(森) 中堅
    Enemy("盗賊",     9, FOLEST,    [12, 13],  70, 25, 10, ARROW),
    Enemy("道化師",   9, FOLEST,    [14, 15],  70, 24, 12, ARROW),
    Enemy("忍者",     8, FOLEST,    [16, 17],  80, 28, 10, SWORD),
    Enemy("賢者",     8, FOLEST,    [18, 19],  75, 22, 14, WIND),
    Enemy("騎士",     7, FOLEST,    [20, 21],  85, 30, 12, SWORD),

    # MOUNTAIN(山) 強豪
    Enemy("聖戦士",   5, MOUNTAIN,  [22, 23], 150, 38, 25, SWORD),
    Enemy("兵士",     5, MOUNTAIN,  [24, 25], 140, 35, 28, SWORD),
    Enemy("魔法戦士", 4, MOUNTAIN,  [26, 27], 160, 42, 22, WIND),
    Enemy("勇者",     4, MOUNTAIN,  [28, 29], 170, 45, 20, SWORD),
    Enemy("魔道士",   4, MOUNTAIN,  [30, 31], 155, 40, 24, WIND),

    # CASTLE(城) ラスボス
    Enemy("狂戦士",   1, CASTLE,    [32, 33], 999, 99, 99, DEATH, True),
]

enemy_now: Enemy      # インスタンス格納用
