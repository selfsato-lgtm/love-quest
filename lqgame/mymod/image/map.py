import pygame
from .. import data
from ..data.app import U, W, H, IMAGE_LAND
from .util import load_chip

# マップ
class Map(pygame.sprite.Sprite):
    # 初期化
    def __init__(self):
        # 基本の初期化
        super().__init__()
        self.image = pygame.Surface((W, H))
        self.rect = pygame.Rect(0, 0, W, H)
        self.images = load_chip(IMAGE_LAND, False)  # 画像読み込み

    # 更新
    def update(self):
        # オフセット位置の計算
        d = data.game.data
        origin_x = (W - U) // 2
        origin_y = (H - U) // 2
        hero_x = d.x * U
        hero_y = d.y * U
        move_x = int((d.x - d.next_x) * d.move_rate * U)
        move_y = int((d.y - d.next_y) * d.move_rate * U)
        offset_x = origin_x - hero_x + move_x
        offset_y = origin_y - hero_y + move_y

        # マップの描画
        self.image.fill((0, 0, 0))  # 画面を塗りつぶす
        for y in range(d.map_h):
            for x in range(d.map_w):
                # 描画の位置と必要判定
                dx = x * U + offset_x
                dy = y * U + offset_y
                if dx + U < 0 or dx >= self.rect.width: continue
                if dy + U < 0 or dy >= self.rect.height: continue

                # 土地の種類を得て、対応する画像を描画
                pos = x + y * d.map_w
                land = d.data_map.map[pos]
                image = self.images[land]
                self.image.blit(image, (dx, dy))
