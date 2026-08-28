import pygame
from .. import data
from ..data.app import U, W, H, IMAGE_CHARA, U_CHARA
from .util import load_chip
from . import chara as chara_mod

# 建物内NPC(マップ座標に固定表示、カメラ移動に合わせてスクロールする)
class NpcSprite(pygame.sprite.Sprite):
    def __init__(self, npc: "data.interior.NPC"):
        super().__init__()
        if len(chara_mod.imgs) == 0:
            chara_mod.imgs = load_chip(IMAGE_CHARA, True, U_CHARA)
        self.src = chara_mod.imgs[npc.img_nums[0]]
        self.tile_x = npc.x
        self.tile_y = npc.y
        self.image = pygame.transform.scale(self.src, (U, U))
        self.rect = pygame.Rect(0, 0, U, U)

    def update(self):
        d = data.game.data
        origin_x = (W - U) // 2
        origin_y = (H - U) // 2
        hero_x = d.x * U
        hero_y = d.y * U
        move_x = int((d.x - d.next_x) * d.move_rate * U)
        move_y = int((d.y - d.next_y) * d.move_rate * U)
        offset_x = origin_x - hero_x + move_x
        offset_y = origin_y - hero_y + move_y

        self.rect.x = self.tile_x * U + offset_x
        self.rect.y = self.tile_y * U + offset_y
