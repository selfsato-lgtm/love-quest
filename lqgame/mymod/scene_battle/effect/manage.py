import pygame
from dataclasses import dataclass
from ...data.app import U, W
from ... import data
from . import action

TIME_MAX = 750      # 最大時間
time_start: int     # 開始時間
RECT = pygame.Rect(U, U, W - U * 2, U * 8)  # 範囲

RED    = pygame.Color(255,   0,   0)
WHITE  = pygame.Color(255, 255, 255)
AQUA   = pygame.Color(  0, 255, 255)
PURPLE = pygame.Color(255,   0, 255)
YELLOW = pygame.Color(255, 255,   0)

# エフェクト引数
@dataclass
class Args:
    time: int
    rate: float
    screen: pygame.Surface

# 初期化
def init():
    global time_start
    time_start = pygame.time.get_ticks()

# 描画
def draw(name: str, screen: pygame.Surface) -> bool:
    # 時間の確認
    time = pygame.time.get_ticks() - time_start
    if time > TIME_MAX: return True
    rate = time / TIME_MAX

    # 描画
    args = Args(time, rate, screen)
    a = data.action
    if name == a.SWORD: action.draw_sword(args, RECT, RED)
    if name == a.FIRE:  action.draw_magic(args, RECT, RED)
    if name == a.HEAL:  action.draw_heal (args, RECT, YELLOW)
    if name == a.ARROW: action.draw_hit  (args, RECT, WHITE)
    if name == a.WIND:  action.draw_sword(args, RECT, AQUA)
    if name == a.DEATH: action.draw_magic(args, RECT, PURPLE)
    return False
