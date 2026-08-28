from pygame import Surface
from .event import GEvent

# シーン
class Scene:
    NAME: str
    async def update(self, screen: Surface, e: GEvent):
        pass

# シーン管理
class Manager:
    now: str = ""
    next: str = ""
    scenes: dict[str, type[Scene]] = {}
    scene: Scene

    # シーンを登録
    @classmethod
    def add_scene(cls, scene: type[Scene]):
        cls.scenes[scene.NAME] = scene

    # 次のシーン名をセット
    @classmethod
    def set_next(cls, name: str):
        cls.next = name # シーン変更予約

    # 更新
    @classmethod
    async def update(cls, screen: Surface, e: GEvent):
        if cls.next == None: return
        if cls.next != cls.now:
            # シーン変更
            cls.now = cls.next
            cls.scene = cls.scenes[cls.now]()
        await cls.scene.update(screen, e)   # 更新
