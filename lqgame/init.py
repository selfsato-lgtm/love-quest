import os, sys
import mymod as m
from mymod.image import font
from mymod.data import game, audio, scene
from mymod.game.scene import Manager

# CWD（カレント ワーキング ディレクトリ）の初期化
def init_cwd():
    #print(os.getcwd())  # CWDの表示
    if getattr(sys, 'frozen', False):
        # EXE化時: image/font/audioはexeに同梱され、_MEIPASSへ展開される
        app_dir = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        # ブラウザ版(pygbag)ではmain.py/init.pyと同じ階層にimage/font/audioがある
        app_dir = os.path.dirname(__file__)
    os.chdir(app_dir)   # CWDの移動
    #print(os.getcwd())  # CWDの表示

# ゲームの初期化
def init_game():
    # データの初期化
    font.init()     # フォントの初期化
    game.data = game.Game.from_blank()   # データ作成
    audio.load_all()    # 音声のロード

    # シーンの追加
    Manager.add_scene(m.SceneTitle)
    Manager.add_scene(m.SceneMap)
    Manager.add_scene(m.SceneBattle)

    # 最初のシーンのセット
    Manager.set_next(scene.TITLE)
    #Manager.set_next(scene.MAP)
    #Manager.set_next(scene.BATTLE)
