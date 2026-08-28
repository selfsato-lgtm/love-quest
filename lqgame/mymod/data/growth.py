from . import game  # 型ヒント用

# 経験値追加
def add_exp(d: "game.Game", exp: int) -> bool:
    d.exp = min(d.exp + exp, 999)
    need = [0, 10, 20, 40, 60, 80, 100, 125, 150, 175, 200,
        250, 300, 350, 400, 500, 600, 700, 800, 900]   # 1～20
    level = 0
    for i, n in enumerate(need):    # 経験値からレベルを計算
        if d.exp >= n: level = i + 1

    is_up = d.level != level  # レベルアップ判定
    if is_up:
        d.level = level
        hp_loss = d.hp_max - d.hp
        mp_loss = d.mp_max - d.mp
        calc_ability(d)     # 能力値の計算
        d.hp = d.hp_max - hp_loss   # HP回復
        d.mp = d.mp_max - mp_loss   # MP回復
    return is_up

# 能力値の計算
def calc_ability(d: "game.Game"):
    # アイテム
    i_at = (d.items.sword.count  -1) * 20
    i_df = (d.items.shield.count -1) * 20

    # 基本値の計算
    d.at = min(10 + (d.level - 1) * 5 + i_at, 999)  # 攻撃力
    d.df = min(10 + (d.level - 1) * 5 + i_df, 999)  # 防御力
    d.hp_max = min(100 + (d.level - 1) * 25, 999)   # 最大HP
    d.mp_max = min(100 + (d.level - 1) * 25, 999)   # 最大MP
