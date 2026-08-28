import pygame
from .. import data, game
from . import proc, view

class SceneBattle(game.scene.Scene):
    NAME = data.scene.BATTLE

    def __init__(self):
        self.sprites = pygame.sprite.RenderUpdates()    # 描画更新用
        self.enemy = view.chara.init()  # キャラ初期化
        self.enemy.add(self.sprites)    # グループ設定

        self.menu = data.action.Menu()  # メニュー
        self.res = data.battle.Res()    # 空Res
        self.proc = data.battle.PROC_MY_WAIT    # 進行

        # 通常/最終戦闘のBGMを開始
        bgm = data.audio.BATTLE
        if data.enemy.enemy_now.is_last: bgm = data.audio.BATTLE_LAST
        game.audio.play_bgm(bgm)

    # 更新
    async def update(self, screen: pygame.Surface, e: game.event.GEvent):
        self.sprites.update()       # スプライト更新
        self.sprites.draw(screen)   # スプライト描画
        view.view.draw(screen, self.menu)   # 全て描画

        # 進行による分岐
        b = data.battle
        p = self.proc
        if p == b.PROC_MY_DRAW:         # 自描画
            is_end = proc.my.draw(self.res, screen)
            if is_end: await proc.my.end(self)
        elif p == b.PROC_ENEMY_DRAW:    # 敵描画
            is_end = proc.enemy.draw(self.res, screen)
            if is_end: await proc.enemy.end(self)
        elif p == b.PROC_MY_WAIT:       # ユーザー操作待機
            await proc.menu.manage(self, e)
