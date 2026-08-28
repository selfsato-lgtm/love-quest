from ... import data
from ...data.app import U, W, H
from ...image.chara import Chara

# キャラクターの初期化
def init() -> Chara:
    c = Chara(data.game.data.img_nums)      # スプライト作成
    c.set_pos((W - U) // 2, (H - U) // 2)   # 位置設定
    return c
