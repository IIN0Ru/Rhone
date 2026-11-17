import pixlib as L
from pixlib import *
import random, json
random.seed(11)
FL = 124   # 바닥선(= 발 위치)
def G(): return L.im
def floor_planks(w, y0, cols=('#7a5232', '#6e4a2c', '#86593a')):
    R(0, y0, w, 150 - y0, cols[0])
    for r, y in enumerate(range(y0, 150, 5)):
        HL(0, y, w, '#4a2e1a')
        x = -(r * 13 % 29)
        while x < w:
            ln = random.randint(18, 34)
            R(x + 1, y + 1, ln - 1, 4, random.choice(cols)); VL(x, y + 1, 4, '#4a2e1a'); HL(x + 1, y + 1, ln - 2, '#9a6a44')
            x += ln
def wainscot(w, y0, y1, col='#6e4426', hi='#8e5a32', sh='#4a2c16'):
    R(0, y0, w, y1 - y0, col); HL(0, y0, w, hi); HL(0, y0 + 1, w, OUT)
    for x in range(0, w, 14): box(x + 2, y0 + 4, 10, y1 - y0 - 7, col, sh, hi)
def wallpaper(w, y0, y1, a, b):
    R(0, y0, w, y1 - y0, a)
    for x in range(0, w, 6):
        for y in range(y0 + 2, y1, 8): P(x + (3 if (y // 8) % 2 else 0), y, b); P(x + (3 if (y // 8) % 2 else 0), y + 1, b)
def exit_door(x):
    box(x - 7, FL - 26, 14, 26, '#2a1a12'); R(x - 6, FL - 25, 12, 25, '#ffcf7a')
    for k in range(8): HL(x - 6, FL - 25 + k * 3, 12, lerp('#ffcf7a', '#f7a35a', k / 8))
    HL(x - 9, FL - 28, 18, '#5a3a22')
def bed(x, w, frame, sheet, blanket, pillow, fancy=False):
    # x = 왼쪽, 바닥 FL
    h = 12 if not fancy else 14
    box(x, FL - 18, 4, 18, frame, lerp(frame, '#ffffff', .2), lerp(frame, '#000000', .3))     # 머리판
    if fancy:
        box(x - 1, FL - 26, 6, 10, frame, lerp(frame, '#ffffff', .2), lerp(frame, '#000000', .3)); P(x + 1, FL - 27, '#f2c14e'); P(x + 2, FL - 27, '#f2c14e')
    box(x + w - 4, FL - 12, 4, 12, frame, lerp(frame, '#ffffff', .2), lerp(frame, '#000000', .3))
    box(x + 3, FL - 10, w - 6, 6, sheet, '#ffffff', lerp(sheet, '#000000', .2))
    box(x + 12, FL - 11, w - 15, 6, blanket, lerp(blanket, '#ffffff', .25), lerp(blanket, '#000000', .3))
    box(x + 4, FL - 13, 9, 4, pillow, '#ffffff', lerp(pillow, '#000000', .2))
    R(x + 3, FL - 4, w - 6, 4, lerp(frame, '#000000', .35))
    if fancy:
        for k in range(x + 14, x + w - 4, 4): P(k, FL - 9, '#f2c14e')
def candle(x, y):
    R(x, y - 4, 2, 4, '#f2ead6'); P(x, y - 5, '#ffcf5a'); P(x + 1, y - 6, '#fff2a8')
    for py in range(y - 12, y + 2):
        for px in range(x - 7, x + 9):
            d = (px - x) ** 2 + (py - y + 6) ** 2
            if 4 < d < 50 and 0 <= px < L.W and 0 <= py < 150:
                p = L.im.getpixel((px, py))
                if p[3]: P(px, py, lerp(p, '#ffd98e', .15))

# ===================== 여관 내부 (390 x 150) =====================
new_canvas(390, 150)
# 천장 들보
R(0, 0, 390, 150, '#3a2416')
# 구역 1: 로비 (0~130)
wallpaper(130, 10, 96, '#b89a6e', '#a8885e')
wainscot(130, 96, FL)
# 구역 2: 일반실 (134~251)
wallpaper(390, 10, 96, '#b89a6e', '#a8885e')
for x0, x1, wp in ((134, 251, ('#9aa88a', '#8a987a')), (255, 390, ('#7a2a3a', '#8e3848'))):
    wallpaper(x1, 10, 96, *wp) if False else None
# 실제 구역별 벽지
def zone_wall(x0, x1, a, b):
    for x in range(x0, x1):
        for y in range(10, 96): P(x, y, a)
    for x in range(x0, x1, 6):
        for y in range(12, 96, 8): P(x + (3 if (y // 8) % 2 else 0), y, b)
zone_wall(0, 130, '#b89a6e', '#a8885e')
zone_wall(134, 251, '#8e9a7a', '#7e8a6c')
zone_wall(255, 390, '#7a2a3a', '#8e3848')
wainscot(390, 96, FL)
# 고급실 금빛 몰딩
HL(255, 96, 135, '#f2c14e'); HL(255, 11, 135, '#f2c14e')
# 천장 들보
R(0, 0, 390, 10, '#4a2e1a'); HL(0, 9, 390, OUT)
for x in range(0, 390, 40): box(x, 0, 8, 12, '#5a3a22', '#7a5232', '#3a2416')
# 칸막이 벽
for x in (130, 251):
    box(x, 0, 4, FL, '#5a3a22', '#7a5232', '#3a2416')
floor_planks(390, FL)
# 고급실 붉은 카펫
R(262, FL, 120, 4, '#a8323e'); HL(262, FL, 120, '#c84a56'); for_k = [P(k, FL + 1, '#f2c14e') for k in range(264, 380, 3)]
# --- 로비
exit_door(17)
# 접수대 (x 67)
box(40, FL - 16, 54, 16, '#7a4e2a', '#9a6a3c', '#4a2e18')
for x in range(44, 92, 8): box(x, FL - 13, 6, 10, '#6a4224', '#8a5a32', '#4a2e18')
HL(38, FL - 17, 58, '#9a6a3c'); HL(38, FL - 18, 58, OUT)
R(80, FL - 21, 6, 3, '#f2c14e'); P(82, FL - 22, '#f2c14e')     # 종
box(46, FL - 22, 8, 4, '#efe3cb')                                  # 장부
# 열쇠걸이
box(48, 40, 34, 18, '#5a3a22', '#7a5232', '#3a2416')
for k in range(5): P(52 + k * 6, 44, '#c8c8d0'); VL(52 + k * 6, 45, 4, '#f2c14e')
# 창문 + 화분
L.window(100, 34, 16, 20, lit=False)
flowerpot(105, FL - 6, '#f25c5c')
# 액자
box(12, 36, 18, 14, '#c48a26'); R(14, 38, 14, 10, '#6a9ab8'); R(14, 44, 14, 4, '#4e7a4a')
# --- 일반실 (침대 x 195 = 780/4)
L.window(150, 34, 14, 18, lit=False, shutters=('#4e7a4a', '#6a9a5e', '#36583a'))
bed(178, 36, '#8a5a32', '#efe3cb', '#5a7ab8', '#f7f2e6')
box(218, FL - 12, 10, 12, '#7a4e2a', '#9a6a3c', '#4a2e18'); candle(222, FL - 12)
box(140, FL - 20, 14, 20, '#7a4e2a', '#9a6a3c', '#4a2e18'); HL(141, FL - 12, 12, '#4a2e18'); P(150, FL - 16, '#f2c14e')   # 옷장
R(234, FL - 3, 12, 3, '#8a6a3a')   # 러그
# --- 고급실 (침대 x 325 = 1300/4)
L.window(270, 26, 18, 26, lit=False, arch=True)
for sx in (266, 289):   # 커튼
    for k in range(30): HL(sx, 24 + k, 4, '#a8323e' if k % 4 else '#c84a56')
bed(300, 48, '#6a3a1e', '#fff8ea', '#a8323e', '#ffffff', fancy=True)
# 샹들리에
VL(330, 10, 8, '#c48a26'); HL(322, 18, 17, '#c48a26')
for k in range(322, 340, 4): candle(k, 22)
# 장식장·와인
box(354, FL - 22, 16, 22, '#6a3a1e', '#8a5a32', '#4a2416'); R(358, FL - 18, 2, 6, '#7a1a2a'); R(363, FL - 18, 2, 6, '#2a5a2a'); HL(355, FL - 11, 14, '#4a2416')
box(272, FL - 10, 14, 10, '#6a3a1e', '#8a5a32', '#4a2416'); R(276, FL - 15, 6, 5, '#e2c84c'); P(278, FL - 17, '#f25c5c'); P(279, FL - 18, '#f25c5c')
box(375, 40, 12, 16, '#c48a26'); R(377, 42, 8, 12, '#3a2a4a'); P(380, 46, '#f2c14e')
# 바닥 그림자 비네트
for x in range(390):
    for y in range(10, 14): P(x, y, lerp(L.im.getpixel((x, y)), '#000000', .25))
L.im.save('/home/claude/pix/int_lodge.png')

# ===================== 마구간 내부 (250 x 150) =====================
new_canvas(250, 150)
R(0, 0, 250, 150, '#2a1a12')
plank_wall(0, 0, 250, FL, ['#5e3e24', '#563820', '#664428'])
# 지붕 트러스
for x in range(0, 250, 50):
    box(x, 0, 6, FL, '#3a2416', '#5a3a22', '#2a1a10')
HL(0, 18, 250, '#3a2416'); HL(0, 19, 250, '#3a2416')
for x in range(0, 250, 50):
    for k in range(16): P(x + 6 + k, 18 - k, '#3a2416'); P(x + 44 - k, 18 - k, '#3a2416')
# 지푸라기 바닥
R(0, FL, 250, 26, '#8a6a32')
for _ in range(900):
    x = random.randint(0, 249); y = random.randint(FL, 149)
    P(x, y, random.choice(('#c9a040', '#e2bc54', '#7a5a2a', '#a8843a')))
HL(0, FL, 250, '#5a4020')
# 출구
exit_door(17)
# 말 칸막이 2개 (x 107, 165)
def stall(cx, coat, mane):
    # 말 (머리가 왼쪽)
    R(cx - 12, FL - 24, 26, 11, coat); HL(cx - 12, FL - 24, 26, lerp(coat, '#ffffff', .2))
    for lx in (cx - 9, cx - 5, cx + 7, cx + 11): R(lx, FL - 13, 3, 13, lerp(coat, '#000000', .2)); R(lx, FL - 2, 3, 2, '#2a1a12')
    R(cx - 17, FL - 34, 7, 12, coat); R(cx - 21, FL - 34, 6, 6, coat); R(cx - 22, FL - 30, 4, 3, lerp(coat, '#000000', .25))
    P(cx - 18, FL - 33, OUT); P(cx - 15, FL - 36, coat); P(cx - 13, FL - 36, coat)
    for k in range(10): P(cx - 11 + (k // 4), FL - 34 + k, mane); P(cx - 10 + (k // 4), FL - 34 + k, mane)
    for k in range(8): P(cx + 14 + (k // 3), FL - 23 + k, mane)
    # 칸막이 문(앞)
    box(cx - 26, FL - 14, 52, 14, '#7a5230', '#9a6a3c', '#4a2e18')
    for k in range(48): P(cx - 24 + k, FL - 13 + int(abs(k - 24) / 24 * 10), '#4a2e18')
    box(cx - 28, FL - 30, 4, 30, '#5a3a22', '#7a5232', '#3a2416'); box(cx + 24, FL - 30, 4, 30, '#5a3a22', '#7a5232', '#3a2416')
    box(cx - 6, FL - 44, 16, 8, '#3a2416', None, None, '#c48a26')
stall(107, '#8e5a34', '#3a2416')
stall(165, '#d8c6a4', '#8a6a4a')
# 건초 침상 (x 217)
for (bx, by) in ((198, FL - 9), (214, FL - 9), (230, FL - 9), (206, FL - 17), (222, FL - 17)):
    box(bx, by, 16, 9, '#e2bc54', '#f2d47a', '#a88430')
    for yy in range(by + 2, by + 8, 3): HL(bx + 1, yy, 14, '#c9a040')
R(206, FL - 20, 22, 4, '#8a7a9a'); HL(206, FL - 20, 22, '#a89ab8')   # 낡은 담요
# 거미줄, 걸린 랜턴, 양동이, 쇠스랑, 말굽
for k in range(12): P(8 + k, 2 + k, '#c8c0b8'); P(8 + k, 2, '#c8c0b8'); P(8, 2 + k, '#c8c0b8')
for k in range(4, 12, 3): HL(8, 2 + k, k, '#a8a098')
L.lantern(60, 30)
box(44, FL - 8, 8, 8, '#7a7a82', '#9a9aa2', '#4a4a52'); HL(44, FL - 9, 8, '#4a4a52')
VL(140, FL - 30, 30, '#7a4e2a'); HL(138, FL - 30, 5, '#8a8a92')
for k in (138, 140, 142): P(k, FL - 31, '#8a8a92')
for k in range(5): P(70 + k, 50 + abs(k - 2), '#8a8a92')
# 벽 틈새로 들어오는 노을빛
for x0 in (30, 80, 190):
    for y in range(24, 90, 1):
        P(x0 + y // 10, y, lerp(L.im.getpixel((x0 + y // 10, y)), '#ffcf7a', .35))
L.im.save('/home/claude/pix/int_stable.png')
print('ok')
