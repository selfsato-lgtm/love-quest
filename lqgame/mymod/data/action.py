from dataclasses import dataclass

SWORD  = "Talk"
FIRE   = "Date"
HEAL   = "Heal"
ESCAPE = "Escape"

ARROW = "Arrow"
WIND  = "Wind"
DEATH = "Death"

@dataclass
class Menu:
    texts = [SWORD, FIRE, HEAL, ESCAPE]
    sel = 0
