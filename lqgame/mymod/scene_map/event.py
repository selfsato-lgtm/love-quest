import random, copy
from dataclasses import dataclass
from .. import data

MES = "message"
BATTLE = "battle"
NONE = "none"
ENTER = "enter"
EXIT = "exit"
MES_MONSTER = "%sとの\n戦闘を開始！"

NAMES = {
    data.map.TOWN:   "街",
    data.map.CASTLE: "魔王城",
    data.map.CAVE:   "洞窟",
}

@dataclass
class Res:
    text: str
    type: str

class Last:
    x:int = -1
    y:int = -1

# 初期化
def init():
    d = data.game.data
    Last.x = d.x    # マップ移動の開始位置
    Last.y = d.y

# 実行確認
def try_exec(x: int, y: int) -> Res:
    d = data.game.data
    res = Res("", NONE)

    # 同じマスで連続発生する対策
    if Last.x == x and Last.y == y: return res
    Last.x = x
    Last.y = y

    land = d.data_map.map[x + y * d.map_w]

    # 建物への入場判定(屋外マップで街/城/洞窟を踏んだ)
    if d.in_building < 0 and land in data.map.INTERIOR_KINDS:
        return Res(NAMES.get(land, "建物") + "に入った", ENTER)

    # 建物からの退場判定(建物内で出口を踏んだ)
    if d.in_building >= 0 and land == data.map.EXIT:
        return Res("外に出た", EXIT)

    # 宿屋のベッド判定(建物内でベッドを踏んだ)
    if d.in_building >= 0 and land == data.map.BED:
        d.hp = d.hp_max
        d.mp = d.mp_max
        return Res("宿屋で休んだ。\nHP/MPが\n全回復した！", MES)

    # 場所固有イベント判定
    for ev in d.map_events:
        if ev.x != x or ev.y != y: continue # イベントマスでない
        if ev.once and ev.is_end: continue  # 初回のみで終了済み

        # イベント処理
        if data.map_event.HEAL in ev.types: # 回復
            d.hp = d.hp_max
            d.mp = d.mp_max
        if data.map_event.ITEM in ev.types: # アイテム
            p = ev.param
            i = data.item
            if p == i.SWORD:  d.items.sword.count  += 1
            if p == i.SHIELD: d.items.shield.count += 1
            if p == i.FIRE:   d.items.fire.count   += 1
            if p == i.HEAL:   d.items.heal.count   += 1
            data.growth.calc_ability(d)     # 能力値の計算

        if ev.once: ev.is_end = True    # 初回のみで終了
        return Res(ev.text, MES)    # イベントあり

    # モンスター遭遇判定(建物内では発生しない)
    for e in data.enemy.ENEMIES:
        if e.land != land: continue
        if random.randrange(e.rate) != 0: continue

        # モンスター処理
        data.enemy.enemy_now = copy.deepcopy(e)     # 現在戦っている敵
        text = MES_MONSTER % e.name
        return Res(text, BATTLE)    # イベントあり

    return res  # イベントなし
