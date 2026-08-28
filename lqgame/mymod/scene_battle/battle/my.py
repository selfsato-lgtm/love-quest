import random
from ... import data
from . import util

# 実行 自分
def exec(action: str) -> data.battle.Res:
    res = data.battle.Res(action)
    a = data.action

    # 逃走
    if action == a.ESCAPE:
        res.is_escape = True
        res.success_escape = random.randrange(2) == 0    # 1/2
        return res

    # その他の行動
    m = data.game.data
    e = data.enemy.enemy_now

    mp = pow = df = 0
    if action == a.SWORD:
        pow = m.at
        df = e.df
    if action == a.FIRE:
        res.se = data.audio.MAGIC
        n = m.items.fire.count
        mp =  n * 30
        pow = 25 + n * 25
        df = e.df // 4
    if action == a.HEAL:
        res.se = data.audio.HEAL
        n = m.items.heal.count
        mp =  n * 20
        pow = 100 + n * 50

    # MPが足りているか確認して終了/消費
    if m.mp < mp: return res
    res.success_mp = True
    m.mp -= mp

    # 回復の場合
    if action == data.action.HEAL:
        heal = random.randrange(pow // 2, pow)
        m.hp = min(m.hp_max, m.hp + heal)
        res.res_num = heal
        return res

    # ダメージの場合
    damage = util.calc_damage(pow, df)
    e.hp = max(0, e.hp - damage)
    res.res_num = damage
    return res
