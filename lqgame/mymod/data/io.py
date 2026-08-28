import os, sys, json
from . import game, item, map, map_event

classes = (game.Game, item.Items, item.Item, map.Map, map_event.Event)

# セーブファイルの保存先(EXE化時は同梱リソースの展開先(_MEIPASS)ではなく、
# exeが実際に置かれているフォルダに保存する。それ以外はCWD基準)
def _save_path() -> str:
    if getattr(sys, 'frozen', False):
        return os.path.join(os.path.dirname(sys.executable), 'save_data.json')
    return 'save_data.json'

class MyEncoder(json.JSONEncoder):
    def default(self, o):
        for cls in classes:
            if isinstance(o, cls):
                return {'_type': cls.__name__, 'value': o.__dict__}
        return json.JSONEncoder.default(self, o)

class MyDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, o):
        if '_type' not in o: return o
        for cls in classes:
            if o['_type'] == cls.__name__:
                return cls(**o['value'])

# JSON保存
def save():
    text = json.dumps(game.data, cls=MyEncoder, indent=2, ensure_ascii=False)
    with open(_save_path(), 'w', encoding='utf-8') as f:
        f.write(text)

# JSON読み込み（戻り値：空文字は成功、それ以外はエラーメッセージ）
def load() -> str:
    p = _save_path()
    if not os.path.isfile(p): return "not found file"
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    game.data = json.loads(text, cls=MyDecoder)
    return ""
