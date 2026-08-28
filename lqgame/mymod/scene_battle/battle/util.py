import random
from ... import data

# ダメージ計算
def calc_damage(pow: int, df: int) -> int:
    damage = random.randrange(pow // 2, pow)
    damage -= random.randrange(0, df)
    damage = min(max(1, damage), 999)
    return damage

# 自分が死んでいるか判定
def is_my_death() -> bool:
    return data.game.data.hp <= 0

# 敵が死んでいるか判定
def is_enemy_death() -> bool:
    return data.enemy.enemy_now.hp <= 0
