from ... import data, game
from .. import battle, effect
from . import growth
from ...image.dialog import a_show
from pygame import Surface  # 型ヒント用
from .. import main  # 型ヒント用

MES_LOSE = "あなたは死にました\nしかし勇者なので\n復活しました"

# 敵アクション開始
def start(p: "main.SceneBattle"):
    p.res = battle.enemy.exec()
    game.audio.play_se(p.res.se)
    effect.manage.init()
    p.proc = data.battle.PROC_ENEMY_DRAW

# 敵アクション描画
def draw(r: data.battle.Res, screen: Surface):
    is_end = effect.manage.draw(r.action, screen)
    effect.sub.draw_num(screen, r.res_num)
    effect.sub.draw_my_damage(screen)
    return is_end

# 敵アクション終了
async def end(p: "main.SceneBattle"):
    if battle.util.is_my_death():   # 自死亡→敗北
        game.audio.play_bgm(data.audio.LOSE)
        await a_show(MES_LOSE)
        await a_show(growth.growth(is_lose = True))

        # 最低限回復させてマップに戻る
        m = data.game.data
        m.hp = max(10, int(m.hp_max * 0.1))
        m.mp = max(10, int(m.mp_max * 0.1))
        game.scene.Manager.set_next(data.scene.MAP)
        return
    p.proc = data.battle.PROC_MY_WAIT
