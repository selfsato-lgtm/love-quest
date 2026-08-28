import pygame
from ... import data, image
from ...data.app import U, IMAGE_ITEM

imgs: list[pygame.Surface] = []

# アイテムの描画
def draw(screen: pygame.Surface):
    global imgs
    if len(imgs) == 0: imgs = image.util.load_chip(IMAGE_ITEM, True)
    d = data.game.data
    imgs2 = list(map(lambda n: imgs[n], d.items.get_image_nums()))

    y = U // 2 + image.font.Size.M * 2
    for i, img in enumerate(imgs2):
        x = U // 2 + int(U * 1.25) * i
        screen.blit(img, (x, y))
