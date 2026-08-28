from dataclasses import dataclass
from . import item
from . import game  # 型ヒント用

ITEM = "item"
HEAL = "heal"
MES_ITEM = "街に到着しました\n%sを獲得"
MES_REST = "街に到着しました\n休息しました"

@dataclass
class Event:
    x: int
    y: int
    once: bool
    text: str
    types: list[str]
    param: str
    is_end: bool = False

# マップからイベントを作成
def gen_event_from_map(d: "game.Game") -> list[Event]:
    e: list[Event] = []
    for i, (x, y) in enumerate(d.data_map.towns):
        # 街イベント 初回
        name = item.NAMES[i % len(item.NAMES)]
        e.append(Event(x, y, True, MES_ITEM % name, [ITEM, HEAL], name))

        # 街イベント 2回目以降
        e.append(Event(x, y, False, MES_REST, [HEAL], ""))
    return e
