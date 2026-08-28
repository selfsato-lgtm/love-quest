from ...game import event
from .. import main  # 型ヒント用
from . import my

# メニュー管理
async def manage(p: "main.SceneBattle", e: event.GEvent):
    # メニュー決定
    if e.key_down == event.K_SEL:
        await my.start(p)    # 自アクション開始
        return

    # メニュー選択（上下ループ）
    if e.key_down == event.K_DOWN: p.menu.sel += 1
    if e.key_down == event.K_UP:   p.menu.sel -= 1
    max = len(p.menu.texts)
    if p.menu.sel < 0 : p.menu.sel = max - 1
    if p.menu.sel >= max : p.menu.sel = 0
