from dataclasses import dataclass
from . import audio

PROC_MY_WAIT = "my_wait"
PROC_MY_DRAW = "my_draw"
PROC_ENEMY_DRAW = "enemy_draw"

@dataclass
class Res:
    action: str = ""
    res_num: int = 0
    se: str = audio.DAMAGE
    success_mp: bool = False
    is_escape: bool = False
    success_escape: bool = False
