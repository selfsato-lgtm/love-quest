from ... import data
from ...data.app import U, W
from ...image.chara import Chara

# キャラクターの初期化
def init() -> Chara:
    scale = 6
    c = Chara(data.enemy.enemy_now.img_nums)    # スプライト作成
    c.set_size(scale)   # サイズ設定
    x = (W - U * scale) // 2
    y = int(U * 2.5)
    c.set_pos(x, y)     # 位置設定
    return c
