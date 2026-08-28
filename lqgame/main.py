import pygame, asyncio
from mymod.image import screen
from mymod.game import event, scene
import init

# メイン
async def main():
    # 初期化
    init.init_cwd()     # CWDの初期化
    pygame.init()       # Pygameを初期化
    screen.init_win()   # ウィンドウの初期化
    init.init_game()    # ゲームの初期化

    # ゲームループ
    while True:
        screen.update_pre() # 更新の前処理
        screen.clear()      # 画面の消去

        e = event.exec()    # イベント実行
        if e.running == False: break    # ゲームの終了

        b = screen.get_buffer() # バッファ取得
        await scene.Manager.update(b, e)    # シーンの更新
        screen.update_post()    # 更新の後処理

        await asyncio.sleep(0)  # ブラウザ(pygbag)側に処理を返す
    # 終了
    pygame.quit()

# 実行
if __name__ == "__main__":
    asyncio.run(main())
