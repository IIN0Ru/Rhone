"""assets/pixellab/final 의 스프라이트를 prototype/art_pl.js 로 묶는다.
규칙: <id>_idle_base.png(1프레임), <id>_walk_Nf.png / <id>_attack_Nf.png (32px 가로 스트립).
파일 이름의 캐릭터 이름 → 게임 키: doyun→player, 그 외는 그대로."""
import base64, io, json, re
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[2]
F = ROOT / 'assets' / 'pixellab' / 'final'
KEY = {'doyun': 'player'}
def uri(im):
    b = io.BytesIO(); im.save(b, 'PNG'); return 'data:image/png;base64,' + base64.b64encode(b.getvalue()).decode()
def strip(p):
    s = Image.open(p).convert('RGBA'); n = s.width // s.height
    return [uri(s.crop((i * s.height, 0, (i + 1) * s.height, s.height))) for i in range(n)]
out = {}
for p in sorted(F.glob('*.png')):
    m = re.match(r'([a-z]+)_(idle_base|walk_\d+f|attack_\d+f)\.png', p.name)
    if not m: continue
    k = KEY.get(m.group(1), m.group(1)); kind = m.group(2)
    d = out.setdefault(k, {})
    if kind == 'idle_base': d['idle'] = [uri(Image.open(p).convert('RGBA'))]
    elif kind.startswith('walk'): d['run'] = strip(p)
    else: d['atk'] = strip(p)
(ROOT / 'prototype' / 'art_pl.js').write_text('// PixelLab 정식 아트 (tools/pixellab/build_art_pl.py 로 생성 — 직접 고치지 말 것)\nObject.assign(SPRITES, ' + json.dumps(out) + ');\n')
print({k: {m: len(v) for m, v in d.items()} for k, d in out.items()})
