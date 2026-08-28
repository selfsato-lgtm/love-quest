from ... import data

MES_EXP = "経験値 %s 獲得"
MES_UP = "レベル %s に上昇"

# 経験値と成長
def growth(is_lose: bool = False) -> str:
    m = data.game.data
    e = data.enemy.enemy_now

    # 経験値とレベルアップ
    exp = max(10, e.hp_max // 10)
    if is_lose == True: exp = 10
    is_up = data.growth.add_exp(m, exp)     # 経験値獲得

    # メッセージ
    text = MES_EXP % exp
    if is_up: text += "\n" + MES_UP % m.level
    return text
