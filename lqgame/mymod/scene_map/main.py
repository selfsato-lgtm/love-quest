import pygame
from .. import data, game, image
from . import event, move, view

MES_SAVE = "データを\n保存しました"

class SceneMap(game.scene.Scene):
    NAME = data.scene.MAP

    def __init__(self):
        self.sprites = pygame.sprite.RenderUpdates()    # 描画更新用
        m = image.map.Map()     # マップの初期化
        m.add(self.sprites)     # グループ設定
        c = view.chara.init()   # キャラの初期化
        c.add(self.sprites)     # グループ設定

        view.view.init()    # 表示初期化
        move.init(self.sprites)     # 移動初期化
        event.init()    # イベント初期化
        game.audio.play_bgm(data.audio.FIELD)  # BGM再生

    # 更新
    async def update(self, screen: pygame.Surface, e: game.event.GEvent):
        self.sprites.update()       # スプライト更新
        self.sprites.draw(screen)   # スプライト描画
        view.view.draw(screen)      # 全描画

        await move.manage_move(e.key_keep)  # 移動管理

        # オプション キー → データ保存
        if e.key_down == game.event.K_OPT:
            data.io.save()
            await image.dialog.a_show(MES_SAVE)
