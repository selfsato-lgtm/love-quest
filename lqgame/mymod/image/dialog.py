import pygame, sys, asyncio
from .. import game
from ..data.app import U, W, H
from . import font, screen

# 表示
def show(buffer: pygame.Surface, texts: list[str]):
    # 背景描画
    rect = pygame.Rect(int(U * 1.5), int(U * 1.5), W - U * 3, H - U * 3)
    pygame.draw.rect(buffer, pygame.Color(32, 32, 32), rect)

    # 文字描画
    line_space = int(font.Size.L * 0.5)
    for i, line in enumerate(texts):
        surface = font.get_surface(line, font.Size.L, font.WHITE)
        h = surface.get_height()
        x = (W - surface.get_width())  / 2
        y = (H - h - (h + line_space) * (len(texts) - 1)) / 2 \
            + (h + line_space) * i
        buffer.blit(surface, (x, y))    # 描画

# 待機付き表示
async def a_show(text: str):
    if len(text) == 0: return
    texts = text.splitlines()
    while True:
        screen.update_pre()     # 更新の前処理

        e = game.event.exec()
        if e.running == False:
            pygame.quit()
            sys.exit()
        if e.key_down == game.event.K_SEL: break  # 終了

        buffer = screen.get_buffer()    # バッファ取得
        show(buffer, texts)
        screen.update_post()    # 更新の後処理

        await asyncio.sleep(0)  # ブラウザ(pygbag)側に処理を返す
