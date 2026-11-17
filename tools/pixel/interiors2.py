from outpath import out
import pixlib as L
from pixlib import *
import random
random.seed(23)
FL = 124
def shade(col, t): return lerp(col, '#000000', t)
def light(col, t): return lerp(col, '#ffffff', t)
def floor_planks(w, y0, cols=('#7a5232', '#6e4a2c', '#86593a'), line='#4a2e1a', hi='#9a6a44'):
    R(0, y0, w, 150 - y0, cols[0])
    for r, y in enumerate(range(y0, 150, 5)):
        HL(0, y, w, line); x = -(r * 13 % 29)
        while x < w:
            ln = random.randint(18, 34); R(x + 1, y + 1, ln - 1, 4, random.choice(cols)); VL(x, y + 1, 4, line); HL(x + 1, y + 1, ln - 2, hi); x += ln
def exit_door(x):
    box(x - 7, FL - 26, 14, 26, '#2a1a12'); R(x - 6, FL - 25, 12, 25, '#ffcf7a')
    for k in range(8): HL(x - 6, FL - 25 + k * 3, 12, lerp('#ffcf7a', '#f7a35a', k / 8))
    HL(x - 9, FL - 28, 18, '#5a3a22')
def glow(x, y, r=10, col='#ffd98e', a=.18):
    for py in range(y - r, y + r + 1):
        for px in range(x - r, x + r + 1):
            d = (px - x) ** 2 + (py - y) ** 2
            if d <= r * r and 0 <= px < L.W and 0 <= py < 150:
                p = L.im.getpixel((px, py))
                if p[3]: P(px, py, lerp(p, col, a * (1 - d / (r * r)) + .04))
def candle(x, y):
    R(x, y - 4, 2, 4, '#f2ead6'); P(x, y - 5, '#ffcf5a'); P(x + 1, y - 6, '#fff2a8')
def mug(x, y): box(x, y - 5, 4, 5, '#c8a86a', '#e2c88e', '#8a6a3a'); HL(x + 1, y - 5, 2, '#fff4e0'); P(x + 4, y - 3, '#8a6a3a')
def bottle(x, y, col): R(x, y - 6, 3, 6, col); P(x + 1, y - 8, col); P(x + 1, y - 7, col); P(x, y - 5, light(col, .4))
def round_table(cx, top='#8a5a32'):
    R(cx - 13, FL - 13, 26, 3, top); HL(cx - 13, FL - 13, 26, light(top, .25)); HL(cx - 12, FL - 10, 24, shade(top, .4))
    R(cx - 1, FL - 10, 3, 10, shade(top, .3)); HL(cx - 5, FL - 1, 11, shade(top, .4))
def stool(cx): R(cx - 3, FL - 7, 7, 2, '#7a4e2a'); VL(cx - 2, FL - 5, 5, '#5a3a1e'); VL(cx + 2, FL - 5, 5, '#5a3a1e')
def plaster_wall(w, y0, y1, a, b):
    R(0, y0, w, y1 - y0, a)
    for _ in range(w * (y1 - y0) // 30): P(random.randint(0, w - 1), random.randint(y0, y1 - 1), b)
def beams(w, col='#4a2e1a'):
    R(0, 0, w, 9, col); HL(0, 9, w, OUT)
    for x in range(6, w, 44): box(x, 0, 7, 12, light(col, .1), light(col, .25), shade(col, .3))

# ======================= 술집 (330) =======================
new_canvas(330, 150)
plank_wall(0, 0, 330, FL, ['#5a3622', '#523020', '#603a24'], vertical=False)
beams(330)
R(0, 92, 330, 3, '#3a2416'); HL(0, 92, 330, '#7a5232')   # 허리 몰딩
floor_planks(330, FL, ('#6a4228', '#5e3a22', '#74482c'))
exit_door(17)
# 벽난로 (x 34~66)
stone_wall(32, FL - 40, 38, 40, base='#7a6e66', dark='#554c46', hi='#988c82', mortar='#3a3430')
R(32, FL - 44, 38, 4, '#5a3a22'); HL(32, FL - 44, 38, '#8a5a32')
R(40, FL - 26, 22, 26, '#1a1012')
for k, col in enumerate(('#e2402e', '#f28a2e', '#ffd34e', '#fff2a8')):
    for i in range(6 - k): P(44 + i * 3 + k, FL - 4 - k * 3 - (i % 2) * 2, col); P(45 + i * 3 + k, FL - 3 - k * 3, col)
R(42, FL - 3, 18, 3, '#3a2416'); glow(51, FL - 10, 18, '#ffb060', .3)
# 사냥 트로피 (멧돼지 머리)
box(44, 52, 14, 10, '#5a3a22'); R(46, 54, 10, 7, '#6e4a3a'); P(47, 56, OUT); P(54, 56, OUT); R(49, 59, 4, 3, '#8a6a5a'); P(46, 60, '#f2ead6'); P(55, 60, '#f2ead6')
# 술통 (x 40, 50 → 160, 200) — 벽난로 앞 대신 왼쪽 문 옆
barrel(24, FL - 13); 
# 의뢰 게시판
box(76, 40, 34, 26, '#8a5a32', '#a87444', '#5a3a1e')
for i, (px, py, w_, h_) in enumerate(((79, 43, 10, 8), (91, 44, 8, 10), (101, 43, 6, 7), (80, 54, 9, 9), (92, 56, 12, 7))):
    R(px, py, w_, h_, '#f2ead6' if i % 2 else '#e2d4b4'); HL(px + 1, py + 2, w_ - 3, '#8a7a6a'); HL(px + 1, py + 4, w_ - 4, '#8a7a6a'); P(px + w_ // 2, py, '#e2402e')
# 창문 2
for wx in (128, 182): L.window(wx, 34, 16, 20, lit=False, cross=True); glow(wx + 8, 44, 10, '#ffcf7a', .12)
# 테이블 3 (82, 150, 207) + 의자 + 잔
for cx in (82, 150, 207):
    stool(cx - 18); stool(cx + 18); round_table(cx); mug(cx - 8, FL - 13); mug(cx + 4, FL - 13)
candle(150, FL - 13)
# 수레바퀴 샹들리에
for cx in (110, 190):
    VL(cx, 9, 12, '#2e2a2c'); L.D.ellipse([cx - 12, 21, cx + 12, 25], outline=c('#5a3a22')); HL(cx - 12, 23, 25, '#5a3a22')
    for k in (-10, -4, 3, 9): candle(cx + k, 22); glow(cx + k, 18, 6, '#ffd98e', .15)
# 바 카운터 (237~328) + 뒷 선반
for sy in (40, 58, 76):
    R(232, sy, 98, 3, '#7a4e2a'); HL(232, sy, 98, '#9a6a3c'); HL(232, sy + 3, 98, '#3a2416')
    for k, bx in enumerate(range(236, 326, 7)):
        if random.random() < .8: bottle(bx, sy, random.choice(('#7a1a2a', '#2a5a2a', '#c8a040', '#4a6aa8', '#8a4a1a')))
for bx in (240, 256, 300, 316): barrel(bx, 82, 1)
box(232, FL - 22, 98, 22, '#6a4026', '#8a5a32', '#3a2416')
for x in range(236, 328, 12): box(x, FL - 18, 10, 14, '#5a3620', '#7a4c2c', '#3a2416')
R(230, FL - 25, 100, 4, '#9a6a3c'); HL(230, FL - 25, 100, '#c48a52'); HL(230, FL - 21, 100, OUT)
for k in range(4): mug(244 + k * 18, FL - 25)
# 큰 맥주통 (탭)
box(300, FL - 44, 22, 18, '#8a5a32', '#a87444', '#5a3a1e'); VL(305, FL - 43, 16, '#4a4a52'); VL(316, FL - 43, 16, '#4a4a52'); R(296, FL - 37, 5, 2, '#c8c8d0')
L.im.save(out('int_tavern.png'))

# ======================= 객잔 (330) =======================
new_canvas(330, 150)
plaster_wall(330, 0, FL, '#efe0c4', '#e2d0b0')
R(0, 0, 330, 10, '#3a3438'); HL(0, 10, 330, '#7a2219')
for x in range(0, 330, 6): P(x + 2, 8, '#5a5258')
R(0, 96, 330, FL - 96, '#7a2219'); HL(0, 96, 330, '#a8402e')
for x in range(4, 330, 10): box(x, 99, 8, 21, '#8a2a20', '#a8402e', '#5a1a14')
floor_planks(330, FL, ('#5a3424', '#4e2c1e', '#64392a'), '#2a1410', '#7a4a34')
exit_door(17)
# 붉은 기둥 (140, 380, 620, 860, 1100 → 35, 95, 155, 215, 275)
for px in (35, 95, 155, 215, 275):
    box(px - 3, 10, 7, FL - 10, '#c2362a', '#e2544a', '#8a2219'); HL(px - 4, 92, 9, '#f2c14e')
# 창살 종이창 + 족자 + 그림
for wx in (45, 165):
    box(wx, 26, 36, 32, '#f7ecd2', None, None, '#5a2a1a')
    for k in range(wx + 4, wx + 36, 5): VL(k, 27, 30, '#8a5a3a')
    for k in range(30, 58, 5): HL(wx + 1, k, 34, '#8a5a3a')
    R(wx + 1, 44, 34, 13, '#ffd98e')
box(108, 22, 14, 50, '#f2ead6', None, None, '#5a3a22'); HL(107, 21, 16, '#3a2416'); HL(107, 72, 16, '#3a2416')
for k in range(6): R(112 + (k % 2), 28 + k * 7, 5, 3, '#2a1a12')        # 붓글씨 느낌
box(226, 24, 40, 26, '#f2ead6', None, None, '#5a3a22')
for k in range(12): P(230 + k * 3, 42 - int(abs(k - 6) * 1.6), '#6a7a8a'); P(230 + k * 3, 43 - int(abs(k - 6) * 1.6), '#6a7a8a')
L.D.ellipse([252, 28, 258, 34], fill=c('#e2402e'))
# 붉은 등롱
for lx in (65, 125, 185, 245, 305):
    VL(lx, 10, 6, OUT); L.D.ellipse([lx - 5, 16, lx + 5, 28], fill=c('#e2402e')); HL(lx - 4, 19, 9, '#b8322a'); HL(lx - 4, 24, 9, '#b8322a')
    P(lx - 2, 18, '#ffb08a'); HL(lx - 1, 29, 3, '#f2c14e'); VL(lx, 30, 3, '#f2c14e'); glow(lx, 22, 12, '#ffb08a', .14)
# 낮은 탁자 (75, 130, 210) + 차 + 만두
for cx in (75, 130, 210):
    R(cx - 14, FL - 12, 28, 3, '#3a2016'); HL(cx - 14, FL - 12, 28, '#5a3424'); VL(cx - 12, FL - 9, 9, '#2a1410'); VL(cx + 11, FL - 9, 9, '#2a1410')
    box(cx - 9, FL - 17, 6, 5, '#e2e8ee', '#ffffff', '#a8b0b8'); L.D.ellipse([cx + 2, FL - 17, cx + 9, FL - 12], fill=c('#f2ead6')); P(cx + 5, FL - 16, '#d8c6a4')
    for sx in (cx - 18, cx + 18): R(sx - 3, FL - 5, 7, 2, '#7a2219'); VL(sx - 2, FL - 3, 3, '#3a2016'); VL(sx + 2, FL - 3, 3, '#3a2016')
# 술 항아리
for jx, jh in ((160, 16), (172, 12)):
    L.D.ellipse([jx - 6, FL - jh, jx + 6, FL], fill=c('#6a3a1e')); R(jx - 3, FL - jh - 2, 7, 3, '#5a2a12'); R(jx - 4, FL - jh + 3, 9, 4, '#e2402e'); P(jx - 3, FL - jh + 3, '#f2c14e')
# 계산대 (265~320) + 주판 + 장부
box(256, FL - 22, 68, 22, '#5a2a1a', '#7a3a24', '#3a1a10')
for x in range(260, 322, 10): box(x, FL - 18, 8, 14, '#6a3020', '#8a4a30', '#3a1a10')
R(254, FL - 25, 72, 4, '#7a3a24'); HL(254, FL - 25, 72, '#a8583a'); HL(254, FL - 21, 72, OUT)
box(270, FL - 31, 16, 6, '#5a3a22'); 
for k in range(5): VL(272 + k * 3, FL - 30, 4, '#c8a86a'); P(272 + k * 3, FL - 29, '#2a1a12')
box(296, FL - 28, 12, 3, '#f2ead6'); HL(297, FL - 27, 9, '#8a7a6a')
# 계단 (위층 객실)
for k in range(8): R(300 + k * 3, FL - 30 - k * 8, 30 - k * 3, 3, '#5a3424') if False else None
L.im.save(out('int_inn.png'))

# ======================= 잡화점 (250) =======================
new_canvas(250, 150)
plank_wall(0, 0, 250, FL, ['#7a6a50', '#706048', '#82725a'], vertical=True)
beams(250, '#5a4a32')
floor_planks(250, FL, ('#8a6a42', '#7e603c', '#94724a'))
exit_door(17)
# 벽 선반 3단 x2 (상품 가득)
def shelf_unit(x0, w):
    box(x0, 22, w, 66, '#5a3a22', '#7a5232', '#3a2416')
    for sy in (40, 58, 76):
        R(x0 + 2, sy, w - 4, 3, '#8a5a32'); HL(x0 + 2, sy, w - 4, '#a87444')
    for k, bx in enumerate(range(x0 + 4, x0 + w - 5, 6)):
        col = random.choice(('#e24c3c', '#4c8ae2', '#5ac85a', '#c85ae2', '#e2c84c'))
        R(bx, 33, 4, 7, col); P(bx, 34, '#ffffff'); R(bx + 1, 31, 2, 2, '#d7dee6')
    for bx in range(x0 + 4, x0 + w - 8, 10):
        L.D.ellipse([bx, 51, bx + 7, 57], fill=c('#d49a4a')); HL(bx + 2, 52, 3, '#f2c47a')
    for bx in range(x0 + 4, x0 + w - 8, 9):
        box(bx, 68, 7, 8, random.choice(('#b88a52', '#8a6a9a', '#6a8a6a')), None, None, '#3a2416')
    for bx in range(x0 + 3, x0 + w - 6, 7):
        R(bx, 80, 5, 8, '#c8b896'); HL(bx, 80, 5, '#8a5a32')
shelf_unit(34, 46); shelf_unit(176, 64)
# 벽에 걸린 무기·방패
for k, wx in enumerate((96, 104, 112)):
    VL(wx, 26, 22, '#d7dee6'); VL(wx + 1, 26, 22, '#a8b0b8'); HL(wx - 2, 44, 6, '#8a5a32'); R(wx, 46, 2, 5, '#5a3a22')
L.D.ellipse([118, 26, 136, 46], fill=c('#8a2a20')); L.D.ellipse([121, 29, 133, 43], fill=c('#c8a040')); P(127, 36, '#8a2a20')
# 말린 약초 줄
HL(140, 18, 34, '#8a7a6a')
for k in range(5): VL(143 + k * 7, 19, 8, '#5a8a3a'); P(142 + k * 7, 26, '#3e6e2e'); P(144 + k * 7, 25, '#7aaa4a')
# 카운터 (130~195) + 저울 + 금고
box(128, FL - 22, 70, 22, '#6a4a2a', '#8a6a3a', '#3a2a16')
for x in range(132, 196, 12): box(x, FL - 18, 10, 14, '#5a3e22', '#7a5a32', '#3a2a16')
R(126, FL - 25, 74, 4, '#9a7a4a'); HL(126, FL - 25, 74, '#c4a46a'); HL(126, FL - 21, 74, OUT)
VL(150, FL - 35, 10, '#c8a040'); HL(143, FL - 35, 15, '#c8a040'); HL(141, FL - 30, 5, '#c8a040'); HL(155, FL - 30, 5, '#c8a040'); VL(143, FL - 34, 4, '#8a7a6a'); VL(157, FL - 34, 4, '#8a7a6a')
box(184, FL - 33, 10, 8, '#5a5a62', '#7a7a82', '#3a3a42'); P(189, FL - 30, '#f2c14e')
# 사과 통, 술통, 러그
barrel(90, FL - 13); 
for k in range(4): L.D.ellipse([91 + k * 2, FL - 16, 94 + k * 2, FL - 13], fill=c('#e24c3c'))
crate(104, FL - 10, 10); crate(214, FL - 10, 10); crate(224, FL - 10, 10); crate(219, FL - 20, 9)
R(46, FL, 60, 3, '#4e6a8a'); HL(46, FL, 60, '#6a8aaa')
L.window(228, 34, 0, 0, lit=False) if False else None
L.im.save(out('int_shop.png'))

# ======================= 수련장 (275) =======================
new_canvas(275, 150)
stone_wall(0, 0, 275, FL, base='#7e7e88', dark='#5a5a64', hi='#9a9aa4', mortar='#3e3e46')
R(0, 0, 275, 8, '#3a3a42'); HL(0, 8, 275, OUT)
exit_door(17)
# 높은 창 빛줄기
for wx in (60, 150, 230):
    box(wx, 14, 12, 18, '#2a2a32'); R(wx + 1, 15, 10, 16, '#ffd9a0'); VL(wx + 6, 15, 16, '#5a5a64')
    for y in range(32, FL):
        for k in range(12):
            xx = wx + k + (y - 32) // 3
            if 0 <= xx < 275: P(xx, y, lerp(L.im.getpixel((xx, y)), '#ffe0a8', .12))
# 깃발
for bx, col in ((96, '#3a4e8a'), (200, '#8a2a2a')):
    box(bx, 12, 20, 36, col, light(col, .2), shade(col, .3))
    for k in range(12): P(bx + 4 + k, 18 + k, '#d7dee6'); P(bx + 15 - k, 18 + k, '#d7dee6')
    for k in range(0, 20, 5): P(bx + k + 2, 48, shade(col, .3)); P(bx + k + 3, 49, shade(col, .3))
# 바닥: 모래 + 매트
R(0, FL, 275, 26, '#c8a878')
for _ in range(500): P(random.randint(0, 274), random.randint(FL, 149), random.choice(('#b89868', '#d8b888', '#a88858')))
HL(0, FL, 275, '#8a6a4a')
R(110, FL, 80, 4, '#6a8a5a'); HL(110, FL, 80, '#8aaa7a')
# 무기 거치대 (45~85)
R(42, FL - 34, 3, 34, '#5a3a22'); R(84, FL - 34, 3, 34, '#5a3a22'); HL(42, FL - 32, 45, '#7a5232'); HL(42, FL - 12, 45, '#7a5232')
for k, (col, h) in enumerate((('#d7dee6', 30), ('#8a5a32', 32), ('#d7dee6', 26), ('#a8b0b8', 30), ('#8a5a32', 28))):
    VL(48 + k * 8, FL - h, h - 2, col); VL(49 + k * 8, FL - h, h - 2, shade(col, .2))
P(64, FL - 33, '#a8b0b8'); HL(62, FL - 34, 5, '#a8b0b8')    # 창
R(72, FL - 30, 5, 4, '#8a8a92')                               # 도끼날
# 허수아비 표적 (75, 190, 225)
for dx_ in (75, 190, 225):
    VL(dx_, FL - 30, 30, '#7a4e2a'); VL(dx_ + 1, FL - 30, 30, '#5a3a1e'); HL(dx_ - 9, FL - 22, 20, '#7a4e2a')
    box(dx_ - 5, FL - 38, 12, 10, '#e2c88e', '#f2dcaa', '#b89a5a'); P(dx_ - 2, FL - 34, OUT); P(dx_ + 3, FL - 34, OUT); HL(dx_ - 1, FL - 31, 3, OUT)
    box(dx_ - 6, FL - 26, 14, 12, '#c8a86a', '#e2c88e', '#8a6a3a')
    L.D.ellipse([dx_ - 3, FL - 23, dx_ + 4, FL - 17], fill=c('#e2402e')); P(dx_, FL - 20, '#f2ead6')
    for k in range(5): P(dx_ - 4 + k * 2, FL - 14 - (k % 2), '#e2c88e')
# 물통·수건
box(128, FL - 10, 10, 10, '#7a7a82', '#9a9aa2', '#4a4a52'); R(129, FL - 9, 8, 2, '#6a9ab8')
R(140, 70, 12, 3, '#5a3a22'); R(142, 73, 8, 9, '#f2ead6'); VL(146, 73, 9, '#e2d0b0')
L.im.save(out('int_train.png'))
print('ok')
