from pygame.mixer import Sound, music

bgm: dict[str, str] = {}
se: dict[str, Sound] = {}
bgm_old: str = ""
is_muted: bool = True  # BGM/SEを鳴らすかどうか(デフォルトはミュート)

# ミュート切替（曲の再生位置は保ったまま音量だけ0/1にする）
def toggle_mute():
    global is_muted
    is_muted = not is_muted
    music.set_volume(0 if is_muted else 1)

# BGMの登録（ogg, mp3）
def add_bgm(id: str, path: str):
    bgm[id] = path

# BGMの再生
def play_bgm(id: str):
    global bgm_old
    if id == bgm_old: return
    bgm_old = id
    music.load(bgm[id])
    music.set_volume(0 if is_muted else 1)
    music.play(-1)

# SEのロード（ogg, wab）
def load_se(id: str, path: str):
    se[id] = Sound(path)

# SEの再生
def play_se(id: str):
    if is_muted: return
    se[id].play()
