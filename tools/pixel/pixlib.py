"""상경 거리 배경 (도트). 가로 1400 x 세로 210, 오른쪽을 향해 걷는 횡스크롤용."""
import random
from PIL import Image, ImageDraw
random.seed(7)
W, H = 980, 150
BASE = 114          # 건물 바닥 = 인도 윗선
WALK_Y = 124        # 캐릭터 발 위치
CURB = 131
im = Image.new('RGBA', (W, H))
D = ImageDraw.Draw(im)
OUT = '#2a1a1f'
def c(h): return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255) if isinstance(h, str) else h
def P(x, y, col):
    if 0 <= x < W and 0 <= y < H: im.putpixel((int(x), int(y)), c(col))
def R(x, y, w, h, col):
    if w > 0 and h > 0: D.rectangle([x, y, x + w - 1, y + h - 1], fill=c(col))
def HL(x, y, w, col): R(x, y, w, 1, col)
def VL(x, y, h, col): R(x, y, 1, h, col)
def box(x, y, w, h, fill, hi=None, sh=None, out=OUT):
    R(x, y, w, h, out); R(x + 1, y + 1, w - 2, h - 2, fill)
    if hi: HL(x + 1, y + 1, w - 2, hi); VL(x + 1, y + 1, h - 2, hi)
    if sh: HL(x + 1, y + h - 2, w - 2, sh); VL(x + w - 2, y + 1, h - 2, sh)
def dither(x, y, w, h, a, b):
    for j in range(h):
        for i in range(w): P(x + i, y + j, a if (i + j) % 2 else b)
def lerp(a, b, t): a, b = c(a), c(b); return tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3)) + (255,)

# ---------------- 공통 부품 ----------------
def shingles(x0, y0, w, rows, base, dark, hi, slope=0):
    """기와/지붕널: 줄마다 엇갈린 반원 무늬"""
    for r in range(rows):
        y = y0 + r * 4
        off = 0 if r % 2 else 3
        R(x0 - r * slope, y, w + 2 * r * slope, 4, base)
        for x in range(x0 - r * slope - off, x0 + w + r * slope, 6):
            HL(x + 1, y + 3, 4, dark); P(x, y + 2, dark); P(x + 5, y + 2, dark); HL(x + 2, y, 2, hi)
    HL(x0 - rows * slope, y0 + rows * 4, w + 2 * rows * slope, OUT)
def gable_roof(x0, y_base, w, peak, base, dark, hi):
    """박공지붕: 위로 갈수록 좁아짐"""
    rows = peak // 4
    for r in range(rows):
        y = y_base - (r + 1) * 4
        inset = int((r + 1) * (w / 2) / (rows + 1))
        R(x0 + inset - 2, y, w - 2 * inset + 4, 4, base)
        off = 0 if r % 2 else 3
        for x in range(x0 + inset - 2 + off, x0 + w - inset + 2, 6):
            HL(x, y + 3, 5, dark); HL(x + 1, y, 2, hi)
        P(x0 + inset - 3, y, OUT); P(x0 + inset - 3, y + 1, OUT); P(x0 + w - inset + 2, y, OUT); P(x0 + w - inset + 2, y + 1, OUT)
    HL(x0 - 3, y_base, w + 6, OUT); HL(x0 - 2, y_base - 1, w + 4, dark)
def plank_wall(x0, y0, w, h, cols, vertical=True):
    for i in range(0, w if vertical else h, 4):
        col = cols[(i // 4) % len(cols)]
        if vertical: R(x0 + i, y0, 4, h, col); VL(x0 + i, y0, h, '#3a2416')
        else: R(x0, y0 + i, w, 4, col); HL(x0, y0 + i, w, '#3a2416')
    for _ in range(w * h // 90):   # 옹이·결
        x = random.randint(x0 + 1, x0 + w - 2); y = random.randint(y0 + 1, y0 + h - 3)
        P(x, y, '#3a2416'); P(x, y + 1, '#4a2e1a')
def stone_wall(x0, y0, w, h, base='#9a8e82', dark='#6e6359', hi='#bdb2a4', mortar='#4e453f'):
    R(x0, y0, w, h, mortar)
    y = y0
    while y < y0 + h:
        sh = random.choice((4, 4, 5))
        x = x0 - random.randint(0, 4)
        while x < x0 + w:
            sw = random.randint(6, 10)
            xa, xb = max(x0, x + 1), min(x0 + w - 1, x + sw - 1)
            if xb > xa:
                tint = random.choice((base, base, lerp(base, dark, .3), lerp(base, hi, .3)))
                R(xa, y + 1, xb - xa, sh - 1, tint)
                HL(xa, y + 1, xb - xa, hi); VL(xb - 1, y + 2, sh - 2, dark); HL(xa + 1, y + sh - 1, xb - xa - 1, dark)
                if random.random() < .1: P(xa + 2, y + 2, dark)
            x += sw
        y += sh
def brick_wall(x0, y0, w, h, base='#a8553e', dark='#7a3a2a', hi='#c87156', mortar='#5a2e24'):
    R(x0, y0, w, h, mortar)
    for r, y in enumerate(range(y0, y0 + h, 4)):
        for x in range(x0 - (4 if r % 2 else 0), x0 + w, 9):
            xa, xb = max(x0, x + 1), min(x0 + w, x + 8)
            if xb > xa:
                t = random.choice((base, base, lerp(base, dark, .35), lerp(base, hi, .25)))
                R(xa, y + 1, xb - xa, 3, t); HL(xa, y + 1, xb - xa, hi if t == base else t)
def window(x, y, w, h, lit=True, shutters=None, box_flowers=None, cross=True, arch=False):
    glass = '#ffd98e' if lit else '#4e6478'; glass2 = '#ffbf5e' if lit else '#3a4c5e'
    box(x - 1, y - 1, w + 2, h + 2, '#5a3a22', '#7a5232', '#3a2414')
    R(x + 1, y + 1, w - 2, h - 2, glass)
    R(x + 1, y + h // 2, w - 2, h - h // 2 - 1, glass2)
    if not lit:
        for k in range(3): P(x + 2 + k, y + 2 + k, '#8ea6ba')
    else:
        P(x + 2, y + 2, '#fff2c8'); P(x + 3, y + 2, '#fff2c8'); P(x + 2, y + 3, '#fff2c8')
    if cross: VL(x + w // 2, y + 1, h - 2, '#5a3a22'); HL(x + 1, y + h // 2, w - 2, '#5a3a22')
    if arch:
        HL(x, y - 2, w, '#5a3a22'); HL(x + 1, y - 3, w - 2, '#5a3a22')
    if shutters:
        for sx in (x - 5, x + w + 1):
            box(sx, y - 1, 4, h + 2, shutters[0], shutters[1], shutters[2])
            for yy in range(y + 1, y + h, 2): HL(sx + 1, yy, 2, shutters[2])
    if box_flowers:
        box(x - 2, y + h + 1, w + 4, 4, '#7a4a2a', '#9a6438', '#4a2a14')
        for k in range(x - 1, x + w + 1, 2):
            P(k, y + h, '#4e8a3a'); P(k, y + h - 1, random.choice(box_flowers)); P(k + 1, y + h, '#3e6e2e')
def door(x, y, w, h, col='#6e4426', hi='#8e5a32', sh='#4a2c16', arch=True, knob='#f2c14e'):
    box(x, y, w, h, col, hi, sh)
    if arch:
        for k in range(1, w // 2): P(x + k - 1, y + max(0, 3 - k), (0, 0, 0, 0)); P(x + w - k, y + max(0, 3 - k), (0, 0, 0, 0))
    for yy in range(y + 3, y + h - 1, 5): HL(x + 2, yy, w - 4, sh)
    VL(x + w // 2, y + 2, h - 3, sh)
    P(x + w - 4, y + h // 2, knob); P(x + w - 4, y + h // 2 + 1, '#c48a26')
def lantern(x, y, glow=True):
    VL(x, y - 6, 6, OUT); box(x - 2, y, 5, 6, '#ffd98e' if glow else '#555558', '#fff2c8', '#e8a040'); HL(x - 3, y - 1, 7, OUT); HL(x - 2, y + 6, 5, OUT)
    if glow:
        for py in range(y - 8, y + 14):
            for px in range(x - 10, x + 11):
                d2 = (px - x) ** 2 + (py - y - 3) ** 2
                if 16 < d2 <= 100 and 0 <= px < W and 0 <= py < H:
                    p = im.getpixel((px, py))
                    if p[3] and p[:3] != c(OUT)[:3]: P(px, py, lerp(p, '#ffd98e', 0.22 if d2 < 50 else 0.1))
def hanging_sign(x, y, w, h, icon, bg='#3a2416', border='#c48a26'):
    HL(x - 4, y - 6, w // 2 + 6, OUT); VL(x - 4, y - 6, 4, OUT)     # 쇠 브래킷
    VL(x + 2, y - 6, 6, '#555558'); VL(x + w - 3, y - 6, 6, '#555558')
    box(x, y, w, h, bg, None, None, border)
    icon(x + w // 2, y + h // 2)
def smoke(x, y):
    for k, (dx, dy, r) in enumerate(((0, 0, 2), (2, -4, 3), (1, -9, 3), (3, -14, 4))):
        D.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=c('#d9c2b4') if k % 2 else c('#cbb0a2'))
def barrel(x, y, s=1):
    w, h = 10 * s, 13 * s
    box(x, y, w, h, '#8a5a32', '#a87444', '#5a3a1e')
    for yy in (y + 2, y + h - 3): HL(x + 1, yy, w - 2, '#4a4a52')
    VL(x + w // 3, y + 1, h - 2, '#6e4426')
def crate(x, y, s=10):
    box(x, y, s, s, '#b88a52', '#d6a86c', '#7a5530')
    for k in range(1, s - 1): P(x + k, y + k, '#7a5530'); P(x + s - 1 - k, y + k, '#7a5530') if k % 2 else None
def tuft(x, y):
    for dx, h in ((0, 3), (1, 4), (2, 2), (3, 3)): VL(x + dx, y - h, h, '#5a8a3a' if dx % 2 else '#3e6e2e')
def flowerpot(x, y, f):
    box(x, y, 7, 6, '#b8603a', '#d47a4a', '#7a3a22')
    for k in range(5): P(x + 1 + k, y - 1, '#4e8a3a'); P(x + 1 + k, y - 2 - (k % 2), f if k % 2 == 0 else '#3e6e2e')



def new_canvas(w, h):
    global im, D, W, H
    W, H = w, h; im = Image.new('RGBA', (w, h)); D = ImageDraw.Draw(im); return im
