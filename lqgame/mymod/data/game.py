from dataclasses import dataclass, field
from . import growth, item, map, map_event

@dataclass
class Game:
    # 主人公
    x: int = 10     # X位置
    y: int = 10     # Y位置
    next_x: int = 10    # 次のX位置
    next_y: int = 10    # 次のY位置
    move_rate: float = 0.0  # 移動比率
    exp: int = 0    # 経験値
    level: int = 0  # レベル
    hp: int = 0     # HP
    mp: int = 0     # MP
    hp_max: int = 0 # 最大HP
    mp_max: int = 0 # 最大MP
    at: int = 0     # 攻撃力
    df: int = 0     # 防御力
    items: item.Items = field(
        default_factory = lambda: item.Items.from_blank())  # アイテム
    img_nums: list[int] = field(default_factory = lambda: [0, 1]) # 画像参照

    # マップ
    map_w: int = 60
    map_h: int = 40
    data_map: map.Map = field(default_factory = lambda: map.Map.from_wh(0, 0))
    map_events: list[map_event.Event] = field(default_factory = list)

    # 建物入場時の退避先(屋外マップに戻るための情報)
    in_building: int = -1   # 入場中の土地種別(-1は屋外)
    saved_map: map.Map | None = None
    saved_map_w: int = 0
    saved_map_h: int = 0
    saved_x: int = 0
    saved_y: int = 0
    building_npcs: list = field(default_factory = list)  # 入場中の建物のNPC(data.interior.NPC)

    # 空引数から生成
    @classmethod
    def from_blank(cls) -> "Game":
        d = Game()
        growth.add_exp(d, 0)    # 経験値追加（レベル1の値を計算）
        d.data_map = map.Map.from_wh(d.map_w, d.map_h)
        d.data_map.gen(d.x, d.y)    # マップ生成
        d.map_events = map_event.gen_event_from_map(d)    # イベント
        return d

data: Game      # インスタンス格納用
