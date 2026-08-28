from ... import data
from . import util

# 実行 敵
def exec() -> data.battle.Res:
    e = data.enemy.enemy_now
    m = data.game.data
    a = data.action
    pow, df = e.at, m.df
    res = data.battle.Res(e.action, success_mp=True)

    # 行動
    if e.action == a.SWORD: pass
    if e.action == a.ARROW: df //= 4
    if e.action == a.WIND: df //= 2; res.se = data.audio.MAGIC
    if e.action == a.DEATH: res.se = data.audio.MAGIC

    # ダメージ
    damage = util.calc_damage(pow, df)
    m.hp = max(0, m.hp - damage)
    res.res_num = damage
    return res
