import pixlib as L
from pixlib import *
import random, math
FL = 124
def shade(col, t): return lerp(col, '#000000', t)
def light(col, t): return lerp(col, '#ffffff', t)
def glow(x, y, r=10, col='#ffd98e', a=.18):
    for py in range(max(0, y - r), min(150, y + r + 1)):
        for px in range(max(0, x - r), min(L.W, x + r + 1)):
            d = (px - x) ** 2 + (py - y) ** 2
            if d <= r * r:
                p = L.im.getpixel((px, py))
                if p[3]: P(px, py, lerp(p, col, a * (1 - d / (r * r)) + .03))
def rock_back(w, base, dark, hi, seed):
    random.seed(seed)
    R(0, 0, w, 150, base)
    # 큰 바위 덩어리
    for _ in range(w // 9):
        cx, cy, r = random.randint(0, w), random.randint(10, FL), random.randint(6, 16)
        tone = random.choice((base, light(base, .06), shade(base, .08)))
        L.D.ellipse([cx - r, cy - r * .7, cx + r, cy + r * .7], fill=c(tone))
        for k in range(-r + 2, r - 2): P(cx + k, int(cy - r * .7 + 1 + abs(k) * .15), hi)
        for k in range(-r + 3, r - 1): P(cx + k, int(cy + r * .7 - 1), dark)
    for _ in range(w * 2): P(random.randint(0, w - 1), random.randint(0, FL), random.choice((dark, hi)))
def ceiling(w, col, dark):
    R(0, 0, w, 10, col)
    x = 0
    while x < w:
        sw = random.randint(5, 12); h = random.randint(6, 26)
        for k in range(h):
            ww = max(1, int(sw * (1 - k / h)))
            HL(x + (sw - ww) // 2, 10 + k, ww, col)
            P(x + (sw - ww) // 2 + ww - 1, 10 + k, dark)
        x += sw + random.randint(4, 20)
def floor_stone(w, base='#4a4048', dark='#2e282e', hi='#62585e'):
    R(0, FL, w, 150 - FL, shade(base, .25))
    for r, y in enumerate(range(FL, 150, 6)):
        x = -random.randint(0, 9)
        while x < w:
            sw = random.randint(9, 18); t = random.choice((base, shade(base, .1), light(base, .05)))
            R(x + 1, y + 1, sw - 2, 5, t); HL(x + 1, y + 1, sw - 2, hi if r == 0 else light(t, .1)); VL(x + sw - 1, y + 1, 5, dark)
            x += sw
    HL(0, FL, w, light(base, .2))
    # 어두워지는 아래쪽
    for y in range(FL + 14, 150):
        for x in range(w): P(x, y, lerp(L.im.getpixel((x, y)), '#000000', (y - FL - 14) / 40))
def torch(x, y):
    R(x, y, 2, 8, '#5a3a22'); R(x - 1, y - 1, 4, 2, '#3a3438')
    for k, col in enumerate(('#e2402e', '#f28a2e', '#ffd34e')): R(x - 1 + (k > 1), y - 3 - k * 2, 4 - k * (k > 1) - (k == 2), 3, col)
    glow(x + 1, y - 4, 22, '#ffb060', .28)
def bones(x):
    HL(x, FL - 1, 6, '#e2d8c4'); P(x - 1, FL - 2, '#e2d8c4'); P(x + 6, FL - 2, '#e2d8c4')
    R(x + 9, FL - 4, 4, 4, '#e2d8c4'); P(x + 10, FL - 3, OUT); P(x + 12, FL - 3, OUT)
def mush(x, col):
    VL(x + 1, FL - 3, 3, '#d8d0c0'); R(x, FL - 5, 4, 2, col); P(x + 1, FL - 5, light(col, .5)); glow(x + 2, FL - 4, 6, col, .2)
def pillar(x, base='#4e464c'):
    R(x, 0, 14, FL, base); VL(x, 0, FL, light(base, .15)); VL(x + 13, 0, FL, shade(base, .35))
    for y in range(6, FL, 9): HL(x + 1, y, 12, shade(base, .2))
    R(x - 2, FL - 4, 18, 4, light(base, .1)); HL(x - 2, FL - 4, 18, light(base, .25))
def exit_hole(x):
    L.D.ellipse([x - 9, FL - 30, x + 9, FL + 6], fill=c('#ffcf9a'))
    L.D.ellipse([x - 7, FL - 27, x + 7, FL + 6], fill=c('#f7a35a'))
    glow(x, FL - 14, 20, '#ffcf9a', .2)
def stairs_down(x):
    R(x - 16, FL - 2, 32, 2, '#2e282e')
    for k in range(5): R(x - 14 + k * 2, FL + k * 3, 28 - k * 4, 3, shade('#4a4048', .15 + k * .15))
    R(x - 12, FL + 15, 24, 11, '#060406')
    for k in range(-16, 17, 4): P(x + k, FL - 3, '#62585e')
def cobweb(x, y, s):
    for k in range(s): P(x + k, y + k, '#c8c0b8'); P(x + k, y, '#c8c0b8'); P(x, y + k, '#c8c0b8')
    for k in range(3, s, 3): HL(x, y + k, k, '#a8a098')
def puddle(x, w): L.D.ellipse([x, FL + 3, x + w, FL + 7], fill=c('#2a3a4a')); HL(x + 3, FL + 4, 4, '#5a7a9a')

def floor(name, w, seed, base, dark, hi, extra):
    random.seed(seed)
    new_canvas(w, 150)
    rock_back(w, base, dark, hi, seed)
    ceiling(w, shade(base, .45), shade(base, .65))
    floor_stone(w)
    extra(w)
    L.im.save(f'/home/claude/pix/dun_{name}.png')

def d1(w):
    for px in (120, 260, 400, 520): pillar(px)
    for tx in (62, 157, 252, 347, 442, 537): torch(tx, 52)
    exit_hole(20)
    for bx in (100, 230, 360, 480): bones(bx)
    for px_, ww in ((180, 14), (300, 10), (430, 16)): puddle(px_, ww)
    for x in range(0, w, 3):     # 이끼
        if random.random() < .25: P(x, FL - 1, '#3e5a3a')
    stairs_down(547)
    # 버려진 수레, 상자
    box(200, FL - 9, 18, 8, '#5a3a22', '#7a5232', '#3a2416'); L.D.ellipse([202, FL - 4, 207, FL + 1], fill=c('#3a2416')); L.D.ellipse([211, FL - 4, 216, FL + 1], fill=c('#3a2416'))
    crate(330, FL - 9, 9); crate(338, FL - 9, 9)
def d2(w):
    for tx in (80, 210, 340, 470): torch(tx, 56)
    exit_hole(20)
    for cx, cy, s in ((40, 10, 16), (225, 10, 20), (380, 10, 14), (520, 10, 18)): cobweb(cx, cy, s)
    for mx in (90, 96, 150, 290, 296, 410, 500): mush(mx, random.choice(('#7ae2c8', '#a87ae2')))
    for bx in (120, 175, 260, 330, 360, 440): bones(bx)
    # 늑대 굴 입구(어두운 굴)
    for gx in (165, 360):
        L.D.ellipse([gx - 16, FL - 26, gx + 16, FL + 4], fill=c('#120c10')); L.D.ellipse([gx - 12, FL - 22, gx + 12, FL + 4], fill=c('#060406'))
        P(gx - 4, FL - 10, '#e2d84c'); P(gx + 2, FL - 10, '#e2d84c')
    # 기사가 묶인 벽 (x 1900/4 = 475): 쇠고리
    for k in (467, 483): box(k, 28, 5, 5, '#5a5a62', '#8a8a92', '#3a3a42')
    stairs_down(547)
def d3(w):
    # 족장의 방: 붉은 깃발, 화로, 왕좌, 금화
    for bx in (60, 140, 300):
        box(bx, 14, 18, 40, '#6a1a14', '#8a2a20', '#4a1010')
        R(bx + 5, 24, 8, 7, '#e2d8c4'); P(bx + 7, 27, OUT); P(bx + 10, 27, OUT); HL(bx + 7, 30, 4, OUT)
        for k in range(0, 18, 4): P(bx + k + 2, 54, '#4a1010')
    for fx in (110, 240, 345):
        R(fx - 5, FL - 14, 10, 3, '#5a5a62'); R(fx - 1, FL - 11, 3, 11, '#4a4a52'); HL(fx - 4, FL - 1, 9, '#4a4a52')
        for k, col in enumerate(('#e2402e', '#f28a2e', '#ffd34e')): R(fx - 4 + k, FL - 17 - k * 3, 9 - 2 * k, 3, col)
        glow(fx, FL - 20, 26, '#ffa050', .3)
    exit_hole(20)
    # 왕좌 (x 1300/4 = 325)
    box(312, FL - 40, 26, 40, '#5a4a3a', '#7a6a52', '#3a2e24')
    R(316, FL - 22, 18, 4, '#8a2a20'); for_k = [P(318 + k * 4, FL - 41, '#e2d8c4') for k in range(5)]
    for k in range(5): R(316 + k * 4, FL - 46, 2, 5, '#e2d8c4')
    # 금화 더미, 보석, 상자
    for gx, gw in ((280, 22), (350, 18)):
        for r in range(4): HL(gx + r * 2, FL - 1 - r, gw - r * 4, '#f2c14e')
        for k in range(gw // 3): P(gx + k * 3 + 1, FL - 2 - (k % 3), '#fff2a8')
    box(296, FL - 9, 12, 9, '#8a5a32', '#a87444', '#5a3a1e'); HL(296, FL - 6, 12, '#f2c14e')
    P(364, FL - 6, '#4cc8e2'); P(366, FL - 5, '#e24c8a')
    for bx in (180, 205, 260): bones(bx)

floor('d1', 575, 5, '#3a3238', '#241e24', '#4e464c', d1)
floor('d2', 575, 9, '#2e3234', '#1a1e20', '#40464a', d2)
floor('d3', 375, 13, '#3a2a2a', '#241818', '#523a38', d3)

# ---------- 늑대 스프라이트 (24x16, 오른쪽 보기) ----------
from PIL import Image
WOLF = [
"........................",
"..................OO....",
".................OgO.O..",
"................OgggOgO.",
"...............OgGGgggO.",
"..O...........OgGggeggO.",
".OgO.........OgGgggggggO",
"OgggOOOOOOOOOgGggggwwOO.",
"OggGGGGGGGGGGGgggggOO...",
".OgGGgggggggggggggO.....",
"..OgggggggggggggggO.....",
"..OgggdddddddddgggO.....",
"..OggO.........OggO.....",
"..OdO...........OdO.....",
"..OdO...........OdO.....",
"..OO............OO......",
]
CW = {'O': '#2a1a1f', 'g': '#8a8a96', 'G': '#b0b0bc', 'd': '#5a5a66', 'e': '#e2d84c', 'w': '#f2ead6'}
def wolf_frame(legs, bob):
    im = Image.new('RGBA', (24, 18))
    rows = [r for r in WOLF]
    for y, row in enumerate(rows):
        if y >= 12: continue
        for x, ch in enumerate(row):
            if ch in CW: im.putpixel((x, y + bob + 1), c(CW[ch]))
    # 다리 4개 (앞 2, 뒤 2)
    for lx, off in legs:
        for k in range(4):
            yy = 12 + bob + 1 + k
            if yy < 18:
                im.putpixel((lx + (off if k > 1 else 0), yy), c('#2a1a1f')); 
                if 0 <= lx + 1 + (off if k > 1 else 0) < 24: im.putpixel((lx + 1 + (off if k > 1 else 0), yy), c('#5a5a66' if k < 3 else '#2a1a1f'))
    return im
idle = [wolf_frame([(3, 0), (6, 0), (15, 0), (18, 0)], b) for b in (0, 0, 1, 1)]
run = [wolf_frame([(3, -1), (6, 1), (15, 1), (18, -1)], 0), wolf_frame([(3, 0), (6, 0), (15, 0), (18, 0)], 1),
       wolf_frame([(3, 1), (6, -1), (15, -1), (18, 1)], 0), wolf_frame([(3, 0), (6, 0), (15, 0), (18, 0)], 1)]
for i, f in enumerate(idle): f.save(f'/home/claude/pix/wolf_idle_{i}.png')
for i, f in enumerate(run): f.save(f'/home/claude/pix/wolf_run_{i}.png')
print('ok')
