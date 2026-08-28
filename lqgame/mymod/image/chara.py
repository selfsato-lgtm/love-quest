import pygame
from ..data.app import U, U_CHARA, IMAGE_CHARA
from .util import load_chip

imgs: list[pygame.Surface] = []

# キャラクター
class Chara(pygame.sprite.Sprite):
    # 初期化
    def __init__(self, img_nums: list[int]):
        super().__init__()
        global imgs
        if len(imgs) == 0: imgs = load_chip(IMAGE_CHARA, True, U_CHARA)  # 画像読み込み(高解像度チップ)
        self.images = list(map(lambda n: imgs[n], img_nums))    # 抜粋
        self.image = self.images[0]
        self.rect = pygame.Rect(0, 0, U, U)
        self.is_shake = False
        self.base_x = 0
        self.base_y = 0

    # 位置
    def set_pos(self, x: int, y: int):
        self.base_x = self.rect.x = x
        self.base_y = self.rect.y = y

    # サイズ
    def set_size(self, rate: int):
        self.rect.width  = int(U * rate)
        self.rect.height = int(U * rate)

    # 揺らす
    def shake(self, is_shake: bool):
        self.is_shake = is_shake

    # 更新
    def update(self):
        t = pygame.time.get_ticks()     # 経過時間
        i = t // 500 % len(self.images)
        image = self.images[i]
        size = (self.rect.width, self.rect.height)
        self.image = pygame.transform.scale(image, size)

        self.rect.x = self.base_x
        self.rect.y = self.base_y
        if self.is_shake:
            t2 = t // 40
            self.rect.x += - U // 2 + int(U * (t2 * 11 % 13 / 13))
            self.rect.y += - U // 2 + int(U * (t2 * 11 % 17 / 17))
