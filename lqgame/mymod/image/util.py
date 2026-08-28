import pygame
from ..data.app import U

# 画像分割(unitを省略すると通常のグリッド単位Uでスライス)
def split(surface: pygame.Surface, is_alpha: bool, unit: int = U) -> list[pygame.Surface]:
    images = []
    w, h = surface.get_size()
    flag_src = pygame.SRCALPHA if is_alpha else 0

    for y in range(0, h, unit):
        for x in range(0, w, unit):
            piece = pygame.Surface((unit, unit), flag_src)
            piece.blit(surface, (0, 0), (x, y, unit, unit))
            images.append(piece)
    return images

# チップ読み込み(unitを省略すると通常のグリッド単位Uでスライス)
def load_chip(p: str, is_alpha: bool, unit: int = U) -> list[pygame.Surface]:
    img = pygame.image.load(p)
    imgs = split(img, is_alpha, unit)
    return imgs
