from dataclasses import dataclass

SWORD  = "勇者の剣"
SHIELD = "勇者の盾"
FIRE   = "炎の魔法"
HEAL   = "光の回復"
NAMES = [SWORD, SHIELD, FIRE, HEAL]

# アイテム
@dataclass
class Item:
    type: str
    count: int = 1

# アイテムのリスト
@dataclass
class Items:
    sword: Item
    shield: Item
    fire: Item
    heal: Item

    # 空引数から生成
    @classmethod
    def from_blank(cls):
        return Items(Item(SWORD), Item(SHIELD), Item(FIRE), Item(HEAL))

    # 画像数値配列の取得
    def get_image_nums(self):
        nums = []
        nums += [0] * self.sword.count
        nums += [1] * self.shield.count
        nums += [2] * self.fire.count
        nums += [3] * self.heal.count
        return nums
