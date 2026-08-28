from ... import data
from ...data.app import U, W, H
from ...image.chara import Chara

# キャラクターの初期化
def init() -> tuple[Chara, Chara]:
    scale = 3
    y = (H - U * scale) // 2

    # 主人公
    c1 = Chara(data.game.data.img_nums) # スプライト作成
    c1.set_size(scale)      # サイズ設定
    c1.set_pos(U // 2, y)   # 位置設定

    # タイトル画面用(狂戦士など男性感の強いキャラは避け、妖精を表示)
    e = data.enemy.ENEMIES[0]
    c2 = Chara(e.img_nums)  # スプライト作成
    c2.set_size(scale)      # サイズ設定
    c2.set_pos(W - U * scale - U // 2, y)   # 位置設定

    return (c1, c2)
