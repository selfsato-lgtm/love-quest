from ..game.audio import add_bgm, load_se

FIELD  = "field"
BATTLE = "battle"
LOSE   = "lose"
ENDING = "ending"
WIN    = "win"
BATTLE_LAST = "battle_last"
MAGIC  = "magic"
HEAL   = "heal"
DAMAGE = "damage"

# 全て読み込み(ブラウザ版はogg形式のみ対応のため、ogg拡張子を使用)
def load_all():
    p = "audio/bgm/maou_bgm_8bit"
    add_bgm(FIELD,  p + "01.ogg")
    add_bgm(BATTLE, p + "18.ogg")
    add_bgm(LOSE,   p + "20.ogg")
    add_bgm(ENDING, p + "22.ogg")
    add_bgm(WIN,    p + "24.ogg")
    add_bgm(BATTLE_LAST, p + "25.ogg")
    p = "audio/se/maou_se_8bit"
    load_se(MAGIC,  p + "03.ogg")
    load_se(HEAL,   p + "08.ogg")
    load_se(DAMAGE, p + "22.ogg")
