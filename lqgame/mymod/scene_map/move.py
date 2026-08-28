import pygame
from .. import data, game, image
from . import event, view

MOVE_CYCLE = 250
last_move = 0
sprite_group: pygame.sprite.RenderUpdates = None
npc_sprites: list = []

# 初期化
def init(sprites: pygame.sprite.RenderUpdates):
    global last_move, sprite_group
    last_move = pygame.time.get_ticks()
    sprite_group = sprites

# 移動管理
async def manage_move(key_keep: str):
    global last_move
    d = data.game.data
    time = pygame.time.get_ticks()

    if time < last_move + MOVE_CYCLE:
        # 移動中処理
        d.move_rate = (time - last_move) / MOVE_CYCLE
        return
    else:
        # 到着処理
        last_move = time
        move_goal(d)    # 到着処理

        # イベント発生判定
        res = event.try_exec(d.x, d.y)
        if res.type != event.NONE:
            if res.type == event.ENTER: enter_building(d)
            if res.type == event.EXIT:  exit_building(d)
            await image.dialog.a_show(res.text)
            if res.type == event.BATTLE:
                game.scene.Manager.set_next(data.scene.BATTLE)
            return

        # NPCに話しかける判定(進もうとした先にNPCがいれば、移動せず会話する)
        npc_text = check_npc_bump(key_keep, d)
        if npc_text:
            await image.dialog.a_show(npc_text)
            return

        move_next(key_keep, d)  # 次回移動処理

# NPCへの接触判定(移動先にNPCがいればその場で会話し、実際には移動しない)
def check_npc_bump(key_keep: str, d: data.game.Game) -> str:
    k = key_keep; e = game.event
    tx, ty = d.x, d.y
    if k == e.K_LEFT:  tx -= 1
    if k == e.K_RIGHT: tx += 1
    if k == e.K_UP:    ty -= 1
    if k == e.K_DOWN:  ty += 1
    for npc in d.building_npcs:
        if npc.x == tx and npc.y == ty:
            return npc.text
    return ""

# 建物に入る(屋外マップを退避し、建物内マップへ切替)
def enter_building(d: data.game.Game):
    global npc_sprites
    land = d.data_map.map[d.x + d.y * d.map_w]
    d.saved_map = d.data_map
    d.saved_map_w = d.map_w
    d.saved_map_h = d.map_h
    d.saved_x = d.x
    d.saved_y = d.y
    d.in_building = land

    interior, npcs = data.interior.build(land)
    d.data_map = interior
    d.map_w = interior.w
    d.map_h = interior.h
    d.x = d.next_x = interior.w // 2
    d.y = d.next_y = interior.h - 2   # 出口の少し手前
    d.building_npcs = npcs

    npc_sprites = [image.npc.NpcSprite(npc) for npc in npcs]
    if sprite_group is not None:
        sprite_group.add(*npc_sprites)

    event.Last.x = d.x
    event.Last.y = d.y
    view.view.init()   # ミニマップ等をサイズ変更後の建物内で再初期化

# 建物から出る(退避しておいた屋外マップへ復帰)
def exit_building(d: data.game.Game):
    global npc_sprites
    if sprite_group is not None and npc_sprites:
        sprite_group.remove(*npc_sprites)
    npc_sprites = []
    d.building_npcs = []

    d.data_map = d.saved_map
    d.map_w = d.saved_map_w
    d.map_h = d.saved_map_h
    d.x = d.next_x = d.saved_x
    d.y = d.next_y = d.saved_y
    d.in_building = -1

    event.Last.x = d.x
    event.Last.y = d.y
    view.view.init()   # ミニマップ等を屋外マップで再初期化

# 到着処理
def move_goal(d: data.game.Game):
    d.move_rate = 0
    d.x = d.next_x
    d.y = d.next_y

# 次回移動処理
def move_next(key_keep: str, d: data.game.Game):
    k = key_keep; e = game.event
    if k == e.K_LEFT  and d.x > 0:           d.next_x = d.x - 1
    if k == e.K_RIGHT and d.x + 1 < d.map_w: d.next_x = d.x + 1
    if k == e.K_UP    and d.y > 0:           d.next_y = d.y - 1
    if k == e.K_DOWN  and d.y + 1 < d.map_h: d.next_y = d.y + 1

    # 通行不可(水・壁)なら戻す
    i = d.next_x + d.next_y * d.map_w
    if d.data_map.map[i] in data.map.BLOCKED:
        d.next_x = d.x
        d.next_y = d.y
