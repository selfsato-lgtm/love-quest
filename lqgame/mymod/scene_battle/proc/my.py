import pygame
from ... import data
from .. import battle, effect
from . import enemy, growth
from ...image.dialog import a_show
from ...game.audio import play_bgm, play_se
from ...game.scene import Manager
from .. import main  # 型ヒント用

MES_ESC_SUCCESS = "逃げるのに\n成功しました"
MES_ESC_FAIL = "逃げるのに\n失敗しました"
MES_MP_FAIL = "MPが足りません"
MES_WIN = "%sを\n倒しました"
MES_ENDING = "あなたは王国を\n救いました"
MES_ENDING2 = "Congratulations!\nYou are the hero!"

# 自アクション開始
async def start(p: "main.SceneBattle"):
    action = p.menu.texts[p.menu.sel]
    r = p.res = battle.my.exec(action)  # 自行動実行

    if r.is_escape == True:   # 逃走
        if r.success_escape == True:    # 逃走成功
            await a_show(MES_ESC_SUCCESS)
            Manager.set_next(data.scene.MAP)
        else:   # 逃走失敗
            await a_show(MES_ESC_FAIL)
            enemy.start(p)
        return

    if r.success_mp == False: # MP不足
        await a_show(MES_MP_FAIL)
        return

    # SEとエフェクト表示
    play_se(r.se)   # SE再生
    effect.manage.init()
    a = data.action
    if r.action == a.SWORD : p.enemy.shake(True)
    if r.action == a.FIRE  : p.enemy.shake(True)
    p.proc = data.battle.PROC_MY_DRAW

# 自アクション描画
def draw(r: data.battle.Res, screen: pygame.Surface):
    is_end = effect.manage.draw(r.action, screen)
    effect.sub.draw_num(screen, r.res_num)
    return is_end

# 自アクション終了
async def end(p: "main.SceneBattle"):
    p.enemy.shake(False)      # 敵の揺れを終了

    if battle.util.is_enemy_death():    # 敵死亡→勝利
        pygame.time.wait(500)
        e = data.enemy.enemy_now
        if e.is_last == False:
            # 通常の敵
            play_bgm(data.audio.WIN)
            await a_show(MES_WIN % e.name + "\n" + growth.growth())
            Manager.set_next(data.scene.MAP)
        else:
            # ラスボス
            play_bgm(data.audio.ENDING)
            await a_show(MES_WIN % e.name)
            await a_show(MES_ENDING)
            await a_show(MES_ENDING2)
            Manager.set_next(data.scene.TITLE)
        return

    enemy.start(p)  # 敵の行動を開始
