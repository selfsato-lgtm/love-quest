import pygame
from ...image import font
from ...data.app import U, W

# 数値
def draw_num(screen: pygame.Surface, num: int):
    x = W // 2
    y = int(U * 4)
    text = str(num)
    font.draw_text(screen, x, y, text, font.Size.L4, font.WHITE, True, True)

# 自ダメージ
def draw_my_damage(screen: pygame.Surface):
    t = pygame.time.get_ticks() // 80
    size = U // 4
    x = - size + size * 2 * (t * 11 % 13 / 13)
    y = - size + size * 2 * (t * 11 % 17 / 17)
    screen.blit(screen, (x, y))
