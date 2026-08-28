import pygame
from .. import data, game, image
from . import view

MES_LOAD = "データを\n読み込みました"
MES_FAIL = "データの読み込みに\n失敗しました\n"

class SceneTitle(game.scene.Scene):
    NAME = data.scene.TITLE

    def __init__(self):
        self.sprites = pygame.sprite.RenderUpdates()    # 描画更新用
        c1, c2 = view.chara.init()  # キャラの初期化
        c1.add(self.sprites)
        c2.add(self.sprites)
        game.audio.play_bgm(data.audio.FIELD)   # BGM再生

    # 更新
    async def update(self, screen: pygame.Surface, e: game.event.GEvent):
        self.sprites.update()       # スプライト更新
        self.sprites.draw(screen)   # スプライト描画
        view.text.draw(screen)      # テキストの描画

        # 選択キー → シーン変更
        if e.key_down == game.event.K_SEL:
            game.scene.Manager.set_next(data.scene.MAP)

        # オプション キー → データ読み込み
        if e.key_down == game.event.K_OPT:
            res = data.io.load()
            mes = MES_LOAD if res == "" else MES_FAIL + res
            await image.dialog.a_show(mes)
