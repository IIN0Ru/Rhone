"""상경 거리 배경 (도트). 가로 1400 x 세로 210, 오른쪽을 향해 걷는 횡스크롤용."""
from outpath import out
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

# ---------------- 하늘 (마음에 들었던 노을 유지) ----------------
sky = ['#f9c48a', '#f7b77a', '#f19c6b', '#e3846a', '#c86b62', '#9a5560', '#6f4258']
bh = 11
for i, col in enumerate(sky):
    R(0, i * bh, W, bh, col)
    if i < len(sky) - 1: dither(0, i * bh + bh - 2, W, 2, col, sky[i + 1])
R(0, len(sky) * bh, W, H, sky[-1])
for r in range(10, 0, -1):
    D.ellipse([210 - r, 50 - r, 210 + r, 50 + r], fill=c('#ffe9c4' if r < 7 else '#ffd59a'))
# 구름
for cx, cy, n in ((90, 20, 4), (430, 14, 6), (690, 28, 3), (880, 18, 5)):
    for k in range(n):
        x = cx + k * 9; y = cy + (k % 2) * 2
        D.ellipse([x, y, x + 16, y + 8], fill=c('#fbd2a8')); HL(x + 3, y + 7, 10, '#e9a688')
# 먼 지붕 실루엣 두 겹
def skyline(y0, col, step, var):
    x = -10
    while x < W:
        w = random.randint(step, step + 22); h = random.randint(var, var + 26)
        R(x, y0 - h, w, h + 60, col)
        if random.random() < .5:   # 뾰족 지붕
            for k in range(w // 2): HL(x + k, y0 - h - (w // 2 - k) // 2, w - 2 * k, col)
        if random.random() < .35: R(x + w // 3, y0 - h - 10, 3, 10, col)
        x += w - 2
skyline(86, '#8a5065', 18, 12)
skyline(96, '#704157', 22, 7)
# 먼 창 불빛
for _ in range(80):
    x = random.randint(0, W); y = random.randint(74, 96)
    if im.getpixel((x, y))[:3] in (c('#704157')[:3], c('#8a5065')[:3]): P(x, y, '#ffcf7a')

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


# ---------------- 건물들 (A 캐릭터 기준: 문 22~26px) ----------------
def roof_rows(x0, y_base, w, rows, step, base, dark, hi, over=4):
    for r in range(rows):
        y = y_base - (r + 1) * 3
        x1 = x0 - over + r * step; x2 = x0 + w + over - r * step
        if x2 - x1 < 4: break
        R(x1, y, x2 - x1, 3, base)
        for x in range(x1 + (0 if r % 2 else 2), x2, 4): HL(x, y + 2, 3, dark); P(x + 1, y, hi)
        P(x1 - 1, y + 1, OUT); P(x1 - 1, y + 2, OUT); P(x2, y + 1, OUT); P(x2, y + 2, OUT)
        if r == rows - 1 or x2 - x1 - 2 * step < 4: HL(x1, y - 1, x2 - x1, OUT)
    HL(x0 - over - 1, y_base, w + 2 * over + 2, OUT)
def stable(x0):
    w, h = 80, 44; y0 = BASE - h
    plank_wall(x0, y0, w, h, ['#8a5a32', '#7a4e2a', '#946238'])
    VL(x0, y0, h, OUT); VL(x0 + w - 1, y0, h, OUT)
    roof_rows(x0, y0, w, 11, 4, '#5a3a2e', '#3e2620', '#7a5040')
    box(x0 + w // 2 - 6, y0 - 15, 12, 10, '#3a2416')
    for k in range(10): VL(x0 + w // 2 - 5 + k, y0 - 10 + (k % 3), 5 - (k % 3), '#e8c45a' if k % 2 else '#c9a040')
    dx, dw, dh = x0 + 26, 30, 30
    box(dx, BASE - dh, dw, dh, '#a87444', '#c48a52', '#6e4426'); VL(dx + dw // 2, BASE - dh + 1, dh - 2, OUT)
    for half in (0, 1):
        hx0 = dx + 1 + half * (dw // 2); hw = dw // 2 - 2
        for k in range(dh - 2):
            t = k / (dh - 2); P(hx0 + int(t * hw), BASE - dh + 1 + k, '#6e4426'); P(hx0 + int((1 - t) * hw), BASE - dh + 1 + k, '#6e4426')
    box(x0 + 6, y0 + 10, 12, 10, '#2a1a12')
    R(x0 + 10, y0 + 12, 4, 7, '#7a4a2a'); R(x0 + 9, y0 + 16, 6, 3, '#8e5a34'); P(x0 + 11, y0 + 13, OUT)
    box(x0 + 60, BASE - 8, 11, 8, '#e2bc54', '#f2d47a', '#a88430'); box(x0 + 66, BASE - 15, 10, 8, '#e2bc54', '#f2d47a', '#a88430')
    VL(x0 + 58, BASE - 18, 18, '#7a4e2a'); HL(x0 + 56, BASE - 18, 5, '#8a8a92'); P(x0 + 56, BASE - 19, '#8a8a92'); P(x0 + 60, BASE - 19, '#8a8a92')
    VL(x0 + w // 2, y0 - 38, 6, OUT); HL(x0 + w // 2 - 3, y0 - 36, 7, OUT)
    return x0 + w // 2
def inn(x0):
    w = 116; h1 = 32; h2 = 32; y1 = BASE - h1; y2 = y1 - h2
    stone_wall(x0, y1, w, h1)
    R(x0 - 2, y2, w + 4, h2, '#efe0c4')
    beam = '#5a3620'
    HL(x0 - 2, y2, w + 4, beam); R(x0 - 3, y1 - 2, w + 6, 2, beam)
    for bx in range(x0 - 2, x0 + w + 2, 29):
        R(bx, y2, 2, h2, beam)
        if bx + 29 <= x0 + w + 2:
            for k in range(h2 - 3): P(bx + 2 + int(k / (h2 - 3) * 26), y2 + 1 + k, beam)
    for wx in (x0 + 8, x0 + 35, x0 + 77, x0 + 102):
        window(wx, y2 + 9, 8, 10, lit=random.random() < .7, shutters=('#4e7a4a', '#6a9a5e', '#36583a'), box_flowers=['#f25c5c', '#ffd34e', '#f29ad6'])
    by = y1 - 7
    R(x0 + 46, by, 26, 2, '#6e4426'); HL(x0 + 46, by - 6, 26, '#7a4c2c')
    for k in range(x0 + 46, x0 + 72, 3): VL(k, by - 5, 5, '#5a3620')
    box(x0 + 52, y2 + 5, 14, 20, '#6e4426', '#8e5a32', '#4a2c16'); window(x0 + 55, y2 + 8, 8, 9, lit=True)
    roof_rows(x0, y2, w, 9, 6, '#8a3a2e', '#5e2219', '#b25a44', over=6)
    box(x0 + w - 26, y2 - 30, 8, 18, '#8e7a6a', '#aa9686', '#6a5a4e'); HL(x0 + w - 27, y2 - 31, 10, '#5a4a40')
    smoke(x0 + w - 22, y2 - 36)
    door(x0 + w // 2 - 7, BASE - 24, 14, 24)
    HL(x0 + w // 2 - 10, BASE - 1, 20, '#6e6359')
    lantern(x0 + w // 2 - 12, BASE - 24); lantern(x0 + w // 2 + 12, BASE - 24)
    for wx in (x0 + 12, x0 + 92): window(wx, y1 + 8, 12, 12, lit=True, arch=True)
    def ic(cx, cy):
        R(cx - 4, cy, 9, 2, '#efe3cb'); R(cx - 4, cy - 2, 3, 2, '#f7bf94'); VL(cx - 5, cy - 2, 4, '#c48a26'); VL(cx + 5, cy - 1, 3, '#c48a26'); P(cx + 3, cy - 4, '#ffe68a')
    hanging_sign(x0 + w - 2, y1 + 3, 16, 11, ic)
    flowerpot(x0 + 2, BASE - 6, '#f25c5c'); flowerpot(x0 + w - 9, BASE - 6, '#ffd34e')
    return x0 + w // 2
def shop(x0):
    w, h = 92, 58; y0 = BASE - h
    brick_wall(x0, y0, w, h, base='#9a8e6e', dark='#6e6450', hi='#b8ab88', mortar='#4e4636')
    VL(x0 - 1, y0, h, OUT); VL(x0 + w, y0, h, OUT)
    roof_rows(x0, y0, w, 8, 6, '#3e6a52', '#2a4a38', '#5a8c6e')
    box(x0 + w // 2 - 6, y0 - 17, 12, 11, '#efe0c4'); window(x0 + w // 2 - 3, y0 - 15, 6, 7, lit=True, cross=False)
    ay = y0 + 14
    for k in range(w + 6):
        col = '#e24c3c' if (k // 4) % 2 else '#fff4e0'
        VL(x0 - 3 + k, ay, 7 + (1 if (k % 4) in (1, 2) else 0), col); P(x0 - 3 + k, ay, '#b8322a' if col == '#e24c3c' else '#e6d6bc')
    HL(x0 - 4, ay - 1, w + 8, OUT)
    box(x0 + 5, ay + 12, 38, 24, '#ffe0a0', '#fff2c8', '#e6b870'); HL(x0 + 6, ay + 24, 36, '#7a5232')
    for i, col in enumerate(('#e24c3c', '#4c8ae2', '#5ac85a', '#c85ae2', '#e2c84c')):
        bx = x0 + 8 + i * 7
        R(bx, ay + 18, 4, 5, col); P(bx, ay + 19, '#ffffff'); R(bx + 1, ay + 16, 2, 2, '#d7dee6')
    for i in range(3): D.ellipse([x0 + 9 + i * 10, ay + 27, x0 + 16 + i * 10, ay + 32], fill=c('#d49a4a')); HL(x0 + 11 + i * 10, ay + 28, 3, '#f2c47a')
    door(x0 + 52, BASE - 24, 13, 24, col='#3e6a52', hi='#5a8c6e', sh='#2a4a38')
    window(x0 + 72, ay + 13, 11, 12, lit=True)
    def ic(cx, cy):
        R(cx - 2, cy - 1, 5, 5, '#4c8ae2'); P(cx - 1, cy, '#bfe0ff'); R(cx - 1, cy - 3, 3, 2, '#d7dee6')
    hanging_sign(x0 + w - 3, y0 + 3, 12, 11, ic)
    crate(x0 + 70, BASE - 8, 8); crate(x0 + 78, BASE - 8, 8); crate(x0 + 74, BASE - 15, 7)
    for k in range(3): P(x0 + 75 + k * 2, BASE - 16, '#e24c3c'); P(x0 + 76 + k * 2, BASE - 17, '#e24c3c')
    barrel(x0 + 42, BASE - 13)
    return x0 + 58
def tavern(x0):
    w, h = 104, 62; y0 = BASE - h
    plank_wall(x0, y0, w, h, ['#6a4028', '#5e3822', '#74462c'], vertical=False)
    VL(x0 - 1, y0, h, OUT); VL(x0 + w, y0, h, OUT)
    stone_wall(x0, BASE - 8, w, 8, base='#7a7068', dark='#5a524c', hi='#958a80')
    roof_rows(x0, y0, w, 9, 6, '#4a2a22', '#2e1814', '#6a3e30')
    box(x0 + 12, y0 - 24, 9, 16, '#7a6a5e', '#968676', '#5a4a40'); smoke(x0 + 16, y0 - 30)
    for wx in (x0 + 6, x0 + 72):
        window(wx, y0 + 20, 26, 17, lit=True, cross=False)
        for k in range(2):
            sx = wx + 4 + k * 10
            D.ellipse([sx, y0 + 25, sx + 5, y0 + 30], fill=c('#a8603a')); R(sx - 1, y0 + 30, 7, 6, '#a8603a')
        HL(wx + 1, y0 + 32, 24, '#7a4a2a'); R(wx + 6, y0 + 30, 2, 2, '#ffe68a'); R(wx + 16, y0 + 30, 2, 2, '#ffe68a')
    box(x0 + 40, BASE - 26, 22, 26, '#2a1a12'); R(x0 + 41, BASE - 25, 20, 13, '#ffcf7a')
    box(x0 + 41, BASE - 18, 10, 13, '#8e5a32', '#a87444', '#5a3a1e'); box(x0 + 51, BASE - 18, 10, 13, '#8e5a32', '#a87444', '#5a3a1e')
    def ic(cx, cy):
        D.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=c('#a87444')); HL(cx - 4, cy - 2, 9, '#4a4a52'); HL(cx - 4, cy + 2, 9, '#4a4a52'); P(cx, cy, '#ffe68a')
    hanging_sign(x0 + 40, y0 + 4, 22, 13, ic)
    barrel(x0 + 1, BASE - 13); barrel(x0 + 11, BASE - 13); barrel(x0 + 6, BASE - 26)
    R(x0 + 78, BASE - 7, 22, 2, '#8e5a32'); VL(x0 + 80, BASE - 5, 5, '#5a3a1e'); VL(x0 + 97, BASE - 5, 5, '#5a3a1e')
    lantern(x0 + 66, BASE - 30)
    return x0 + 51
def kaejan(x0):
    w, h = 116, 58; y0 = BASE - h
    R(x0, y0, w, h, '#efe0c4')
    for px in (x0, x0 + 28, x0 + 84, x0 + w - 5):
        box(px, y0, 5, h, '#c2362a', '#e2544a', '#8a2219')
    for wx in (x0 + 7, x0 + 91):
        box(wx, y0 + 12, 19, 22, '#f7ecd2', None, None, '#5a2a1a')
        for k in range(wx + 3, wx + 19, 4): VL(k, y0 + 13, 20, '#8a5a3a')
        for k in range(y0 + 15, y0 + 34, 4): HL(wx + 1, k, 17, '#8a5a3a')
        R(wx + 1, y0 + 24, 17, 9, '#ffd98e')
    box(x0 + 35, BASE - 34, 46, 34, '#7a2219')
    box(x0 + 38, BASE - 30, 20, 30, '#a8402e', '#c8584a', '#7a2219'); box(x0 + 58, BASE - 30, 20, 30, '#a8402e', '#c8584a', '#7a2219')
    for dx in (x0 + 41, x0 + 61):
        for k in range(3):
            for j in range(3): P(dx + 2 + k * 5, BASE - 25 + j * 8, '#f2c14e')
    box(x0 + 41, y0 + 3, 34, 10, '#2a1a12', None, None, '#c48a26')
    for k in range(3): R(x0 + 46 + k * 9, y0 + 5, 6, 6, '#f2c14e'); R(x0 + 48 + k * 9, y0 + 7, 2, 2, '#2a1a12')
    ry = y0 - 3
    for r in range(8):
        y = ry - r * 3; x1, x2 = x0 - 12 + r * 6, x0 + w + 12 - r * 6
        R(x1, y, x2 - x1, 3, '#3a3438')
        for x in range(x1 + (0 if r % 2 else 2), x2, 4): HL(x, y + 2, 3, '#221e22'); P(x + 1, y, '#5a5258')
    HL(x0 + 36, ry - 22, w - 72, OUT)
    R(x0 - 14, ry + 3, w + 28, 2, '#7a2219'); HL(x0 - 14, ry + 3, w + 28, '#a8402e')
    for side in (-1, 1):
        ex = x0 - 14 if side < 0 else x0 + w + 13
        for k in range(5): P(ex - side * (k // 2), ry + 2 - k, '#3a3438'); P(ex - side * (k // 2), ry + 3 - k, '#221e22')
    R(x0 + w // 2 - 1, ry - 25, 3, 2, '#f2c14e')
    for lx in (x0 + 16, x0 + 98):
        VL(lx, ry + 5, 3, OUT)
        D.ellipse([lx - 4, ry + 8, lx + 4, ry + 17], fill=c('#e2402e')); HL(lx - 3, ry + 10, 7, '#b8322a'); HL(lx - 3, ry + 14, 7, '#b8322a')
        P(lx - 2, ry + 9, '#ffb08a'); HL(lx - 1, ry + 18, 3, '#f2c14e'); VL(lx, ry + 19, 2, '#f2c14e')
    for k in range(2): HL(x0 + 33 - k * 2, BASE - 1 - k, 50 + k * 4, '#9a8e82' if k % 2 else '#7a7068')
    VL(x0 + w + 6, BASE - 50, 50, '#5a3a22'); R(x0 + w + 7, BASE - 48, 8, 18, '#e2402e')
    for k in range(3): R(x0 + w + 9, BASE - 45 + k * 5, 4, 2, '#fff4e0')
    return x0 + 58
def alley(x0):
    w = 76; top = 44
    R(x0, top, w, BASE - top, '#241c1c')
    stone_wall(x0, top, 10, BASE - top, base='#5e534e', dark='#463d39', hi='#6e625c', mortar='#2e2624')
    stone_wall(x0 + w - 10, top, 10, BASE - top, base='#5e534e', dark='#463d39', hi='#6e625c', mortar='#2e2624')
    for k in range(w - 20): VL(x0 + 10 + k, top, BASE - top, lerp('#1c1616', '#2e2424', 1 - abs(k - (w - 20) / 2) / ((w - 20) / 2)))
    # 골목 안쪽 먼 벽과 창
    R(x0 + 18, top + 18, w - 36, BASE - top - 18, '#2e2424')
    window(x0 + w // 2 - 4, top + 26, 8, 9, lit=True)
    for rx in (x0 - 2, x0 + w - 12):
        for r in range(3): R(rx + r, top - (r + 1) * 3, 14 - 2 * r, 3, '#3a3438'); P(rx + r + 1, top - (r + 1) * 3, '#5a5258')
        HL(rx - 1, top, 16, OUT)
    for k in range(w - 20): P(x0 + 10 + k, 58 + int(((k - (w - 20) / 2) ** 2) / 80), '#8a7a6a')
    for i, col in enumerate(('#e2c84c', '#4c8ae2', '#fff4e0')):
        cx = x0 + 18 + i * 14; cy = 58 + int(((cx - x0 - 10 - (w - 20) / 2) ** 2) / 80)
        box(cx, cy, 7, 8 - (i % 2) * 2, col)
    barrel(x0 + 12, BASE - 13); crate(x0 + 24, BASE - 8, 8); crate(x0 + 52, BASE - 9, 9)
    box(x0 + 62, BASE - 9, 7, 9, '#5a6a5a', '#7a8a7a', '#3a4a3a')
    # 고양이(밝은 주황 줄무늬로 보이게)
    R(x0 + 40, BASE - 4, 6, 3, '#d9883a'); R(x0 + 44, BASE - 6, 3, 3, '#d9883a'); P(x0 + 44, BASE - 7, '#d9883a'); P(x0 + 46, BASE - 7, '#d9883a')
    P(x0 + 45, BASE - 5, OUT); VL(x0 + 39, BASE - 6, 3, '#d9883a'); P(x0 + 42, BASE - 4, '#a8602a')
    for k in range(3): D.ellipse([x0 + 32 + k, BASE - 10 - k * 4, x0 + 36 + k * 2, BASE - 7 - k * 4], fill=c('#6e6060'))
    box(x0 + 1, 74, 8, 10, '#d8c6a4', None, None, '#8a7a6a'); HL(x0 + 3, 77, 4, '#8a5a3a'); HL(x0 + 3, 79, 3, '#8a5a3a')
    return x0 + w // 2
def dojo(x0):
    w, h = 104, 60; y0 = BASE - h
    stone_wall(x0, y0, w, h, base='#8e8e96', dark='#64646e', hi='#ababb4', mortar='#44444c')
    R(x0 - 2, y0 - 4, w + 4, 4, '#64646e'); HL(x0 - 2, y0 - 4, w + 4, '#ababb4')
    for k in range(x0 - 2, x0 + w + 2, 9): box(k, y0 - 9, 5, 6, '#8e8e96', '#ababb4', '#64646e')
    box(x0 + 36, BASE - 32, 32, 32, '#2a2226'); R(x0 + 37, BASE - 31, 30, 30, '#5a4636'); R(x0 + 37, BASE - 8, 30, 7, '#7a6250')
    for k in range(3): VL(x0 + 41 + k * 10, BASE - 27, 20, '#8a6a4a')
    D.ellipse([x0 + 47, BASE - 27, x0 + 57, BASE - 17], fill=c('#e2d8c4')); D.ellipse([x0 + 49, BASE - 25, x0 + 55, BASE - 19], fill=c('#e2402e'))
    box(x0 + 32, BASE - 32, 5, 32, '#8a5a32', '#a87444', '#5a3a1e'); box(x0 + 67, BASE - 32, 5, 32, '#8a5a32', '#a87444', '#5a3a1e')
    for bx in (x0 + 8, x0 + 80):
        box(bx, y0 + 7, 16, 24, '#3a4e8a', '#4e66a8', '#2a3a6a')
        for k in range(10): P(bx + 3 + k, y0 + 11 + k, '#d7dee6'); P(bx + 12 - k, y0 + 11 + k, '#d7dee6')
        for k in range(0, 16, 4): P(bx + k + 2, y0 + 31, '#2a3a6a')
    for dx_ in (x0 + 4, x0 + 88):
        VL(dx_ + 4, BASE - 18, 18, '#7a4e2a'); HL(dx_, BASE - 14, 9, '#7a4e2a')
        box(dx_ + 1, BASE - 24, 7, 7, '#e2c88e', '#f2dcaa', '#b89a5a'); P(dx_ + 3, BASE - 21, OUT); P(dx_ + 5, BASE - 21, OUT)
        R(dx_ + 2, BASE - 17, 5, 6, '#c8a86a')
    R(x0 + 74, BASE - 16, 1, 16, '#5a3a22'); R(x0 + 84, BASE - 16, 1, 16, '#5a3a22'); HL(x0 + 74, BASE - 14, 11, '#5a3a22')
    for k, col in enumerate(('#d7dee6', '#8a5a32', '#d7dee6')): VL(x0 + 77 + k * 3, BASE - 20, 18, col)
    return x0 + 52
def gate_and_outskirts(x0):
    stone_wall(x0, 36, 74, BASE - 36, base='#8a8078', dark='#625a54', hi='#a69c92', mortar='#45403c')
    for k in range(x0, x0 + 74, 10): box(k, 29, 6, 8, '#8a8078', '#a69c92', '#625a54')
    gx = x0 + 23
    R(gx, 72, 28, BASE - 72, '#1a1416'); D.ellipse([gx, 62, gx + 27, 82], fill=c('#1a1416'))
    for k in range(gx + 2, gx + 27, 4): VL(k, 66, BASE - 66, '#3a3034')
    for k in range(72, BASE, 5): HL(gx + 1, k, 26, '#3a3034')
    box(x0 + 27, 46, 20, 8, '#2a1a12', None, None, '#c48a26')
    R(x0 + 74, 88, W - x0 - 74, BASE - 88, '#4a6a3a')
    for k in range(x0 + 74, W, 3): VL(k, BASE - 2 - (k % 4), 2 + (k % 4), '#5a8a3a')
    for tx in (x0 + 84, x0 + 106, x0 + 176):
        box(tx + 4, BASE - 15, 4, 15, '#6a4628', '#7e5634', '#4a2e18')
        for r_, cy in ((10, BASE - 23), (8, BASE - 33), (5, BASE - 40)):
            D.ellipse([tx + 6 - r_, cy - r_ // 1.4, tx + 6 + r_, cy + r_ // 1.4], fill=c('#3e6e2e')); D.ellipse([tx + 6 - r_ + 2, cy - r_ // 1.4, tx + 6 + r_ - 4, cy], fill=c('#5a8a3a'))
    cx = x0 + 142
    D.ellipse([cx - 22, 70, cx + 22, BASE + 14], fill=c('#5e5450')); D.ellipse([cx - 12, 86, cx + 12, BASE + 12], fill=c('#0e0a0c'))
    for k in range(-9, 10, 4): P(cx + k, 88 + abs(k) // 3, '#e2d8c4')
    lantern(cx - 19, BASE - 22); lantern(cx + 19, BASE - 22)
    return cx

anchors = {}
anchors['마구간'] = stable(10)
anchors['여관'] = inn(104)
anchors['잡화점'] = shop(236)
anchors['술집'] = tavern(342)
anchors['객잔'] = kaejan(466)
anchors['뒷골목'] = alley(598)
anchors['수련장'] = dojo(684)
anchors['던전'] = gate_and_outskirts(800)

# ---------------- 인도·연석·길 ----------------
R(0, BASE, W, CURB - BASE, '#8a7a6c')
for row in range(2):
    x = -random.randint(0, 8); yy = BASE + row * 8
    while x < W:
        sw = random.randint(10, 19)
        R(x + 1, yy + 1, sw - 2, 7, random.choice(('#a8988a', '#9e8e80', '#b2a294')))
        HL(x + 1, yy + 1, sw - 2, '#c4b4a4'); VL(x + sw - 2, yy + 2, 6, '#7a6c60')
        if random.random() < .12:
            for k in range(3): P(x + 3 + k, yy + 3 + k // 2, '#6e6054')
        x += sw
R(0, CURB, W, 3, '#c4b8aa'); HL(0, CURB, W, '#e2d8cc'); HL(0, CURB + 2, W, '#6e6258')
for k in range(0, W, 16): VL(k, CURB, 3, '#8a7e72')
R(0, CURB + 3, W, H - CURB - 3, '#4e4038')
for row, yy in enumerate(range(CURB + 4, H, 5)):
    x = -(row * 4 % 9)
    while x < W:
        sw = random.randint(5, 8)
        tone = random.choice(('#7a6a5c', '#6e5e52', '#857464', '#665648'))
        R(x + 1, yy, sw - 2, 4, tone); HL(x + 2, yy, sw - 4, lerp(tone, '#ffffff', .2)); HL(x + 2, yy + 3, sw - 4, lerp(tone, '#000000', .3))
        x += sw
for px_, w_ in ((300, 22), (640, 16), (770, 24)):
    D.ellipse([px_, 141, px_ + w_, 147], fill=c('#c98a7a')); D.ellipse([px_ + 2, 142, px_ + w_ - 5, 145], fill=c('#e8a888')); HL(px_ + 4, 143, 4, '#ffd2a8')
for gx in (200, 520, 720):
    box(gx, CURB, 10, 4, '#2a2426')
    for k in range(gx + 2, gx + 9, 2): VL(k, CURB + 1, 2, '#5a5458')
for k in range(0, 800, 29):
    if random.random() < .6: tuft(k + random.randint(0, 15), BASE + 1)
def streetlamp(x):
    R(x, BASE - 36, 2, 36 + 6, '#2e2a2c'); HL(x - 2, BASE + 5, 6, '#2e2a2c'); R(x - 1, BASE - 6, 4, 2, '#3e3a3c')
    HL(x - 2, BASE - 38, 6, '#2e2a2c'); lantern(x + 1, BASE - 36)
for lx in (96, 228, 336, 458, 590, 678, 790):
    streetlamp(lx)

im.save(out('street2.png'))
import json; json.dump({'anchors': anchors, 'walk_y': WALK_Y, 'w': W, 'h': H}, open(out('street2.json'), 'w'), ensure_ascii=False)
print('ok', anchors)
