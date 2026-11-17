"""레이어 방식 도트 캐릭터: 부위마다 외곽선을 따로 둘러서 겹치는 곳에 안쪽 선이 생긴다."""
from PIL import Image

OUT = '#2a1a1f'
def hx(h): return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), 255)

PAL_DOYUN = dict(
    skin=('#ffe2c2', '#f7bf94', '#d9916a', '#b56d4c'),
    hair=('#c07a44', '#8f5129', '#683519', '#45200d'),
    shirt=('#fffaf0', '#efe3cb', '#cdbb98', '#a8946e'),
    vest=('#b07a46', '#8a5a30', '#663f1f', '#472a12'),
    pants=('#7d90b4', '#5b6d92', '#435071', '#2f3852'),
    boots=('#8c5a34', '#683f22', '#4a2a14', '#33190a'),
    belt=('#6b4526', '#4f3119', '#3a2210', '#2a170a'),
    gold=('#ffe68a', '#f2c14e', '#c48a26', '#8a5a12'),
    steel=('#ffffff', '#d7dee6', '#9aa6b4', '#6c7888'),
    eye='#2a1a1f', eyelite='#ffffff', iris='#5a3a2a', blush='#f59a86', mouth='#b0583e', brow='#683519')

def rect(x0, y0, w, h): return {(x, y) for x in range(x0, x0 + w) for y in range(y0, y0 + h)}
def ell(cx, cy, rx, ry):
    return {(x, y) for x in range(int(cx - rx) - 1, int(cx + rx) + 2) for y in range(int(cy - ry) - 1, int(cy + ry) + 2)
            if ((x + .5 - cx) / rx) ** 2 + ((y + .5 - cy) / ry) ** 2 <= 1.0}
def rrect(x0, y0, w, h, r):
    p = rect(x0, y0, w, h)
    for i in range(r):
        for j in range(r - i):
            for (ax, ay) in ((x0 + i, y0 + j), (x0 + w - 1 - i, y0 + j), (x0 + i, y0 + h - 1 - j), (x0 + w - 1 - i, y0 + h - 1 - j)):
                if i + j < r: p.discard((ax, ay))
    return p

class Layer:
    def __init__(s): s.px = {}
    def fill(s, pts, ramp, mode='soft'):
        """ramp: (hi, mid, dark, deep). 빛은 왼쪽 위에서."""
        pts = set(pts)
        if not pts: return
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        for (x, y) in pts:
            right = (x + 1, y) not in pts; bottom = (x, y + 1) not in pts
            left = (x - 1, y) not in pts; top = (x, y - 1) not in pts
            c = ramp[1]
            if mode == 'flat': pass
            else:
                if right or bottom: c = ramp[2]
                if (right and bottom) or ((x + 2, y) not in pts and (x, y + 2) not in pts and x > (x0 + x1) / 2): c = ramp[2]
                if (left or top) and not (right or bottom): c = ramp[0]
                if mode == 'round' and x >= x1 - (x1 - x0) // 4 and y >= y0 + (y1 - y0) // 3: c = ramp[2] if c != ramp[0] else ramp[1]
            s.px[(x, y)] = c
    def put(s, x, y, c): s.px[(x, y)] = c
    def outlined(s):
        out = dict(s.px)
        for (x, y) in s.px:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in s.px: out.setdefault(q, OUT)
        return out

def compose(layers, W, H):
    im = Image.new('RGBA', (W, H))
    for L in layers:
        for (x, y), c in L.outlined().items():
            if 0 <= x < W and 0 <= y < H: im.putpixel((x, y), hx(c))
    return im

def doyun(H=32, heads=2.5, frame=0, pal=PAL_DOYUN):
    hh = round(H / heads)
    W = hh + 18
    cx = W // 2 + 1
    ground = H + 2                         # 발바닥 행
    bob = 1 if frame in (1, 3) else 0
    body = ground - hh - 1                  # 목부터 발까지
    torso_h = round(body * (0.47 if heads < 2.8 else 0.44))
    tw = max(7, round(hh * 0.66))
    tx = cx - tw // 2 - 1
    ty = hh + 1 + bob - 2                   # 턱 아래로 살짝 겹치게
    leg_top = ty + torso_h - 2
    lw = max(3, round(tw * 0.42))
    boot_h = max(2, round((ground - leg_top) * 0.3))
    step = {0: 2, 1: 0, 2: -2, 3: 0}[frame]
    layers = []

    def leg(x, lift, ramp_p, ramp_b):
        L = Layer()
        h = ground - leg_top - boot_h - lift
        L.fill(rect(x, leg_top, lw, h), ramp_p)
        bt = rrect(x, ground - boot_h - lift, lw + 1, boot_h, 1)
        L.fill(bt, ramp_b)
        for xx in range(x, x + lw + 1): L.put(xx, ground - lift - 1, ramp_b[3]) if (xx, ground - lift - 1) in bt else None
        return L
    dark = lambda r: (r[1], r[2], r[3], r[3])
    # 뒷다리, 뒷팔
    layers.append(leg(tx + 1 - step, 1 if frame == 0 else 0, dark(pal['pants']), dark(pal['boots'])))
    aw = max(2, round(hh * 0.24)); ah = torso_h - 1
    sw = -step // 2
    BA = Layer(); BA.fill(rrect(tx - aw + 2 + sw, ty + 1, aw, ah - 2, 1), dark(pal['shirt']))
    BA.fill(rrect(tx - aw + 2 + sw, ty + ah - 3, aw, max(2, aw), 1), dark(pal['skin'])); layers.append(BA)
    # 등에 멘 검
    SW = Layer()
    n = torso_h + hh // 2
    for i in range(n):
        x = tx - 2 + (i * 2) // 3; y = ty - hh // 2 + i
        if i < 3: SW.put(x, y, pal['gold'][2] if i else pal['gold'][1])
        elif i == 3:
            for d in (-1, 0, 1): SW.put(x + d, y, pal['gold'][1])
        else: SW.put(x, y, pal['steel'][1] if i % 3 else pal['steel'][0])
    layers.append(SW)
    # 앞다리
    layers.append(leg(tx + tw - lw - 1 + step, 1 if frame == 2 else 0, pal['pants'], pal['boots']))
    # 몸통 (어깨가 둥근 사다리꼴)
    T = Layer()
    torso = rrect(tx, ty, tw, torso_h, 2)
    T.fill(torso, pal['shirt'], 'round')
    # 조끼: 앞섶만 셔츠가 보이게
    open_x = tx + tw - 4
    vest = {(x, y) for (x, y) in torso if not (open_x <= x <= open_x + 1 and y < ty + torso_h - 2) and x < tx + tw - 1}
    T.fill(vest, pal['vest'], 'round')
    for y in range(ty + 2, ty + torso_h - 2, 2): T.put(open_x - 1, y, pal['gold'][1])
    # 셔츠 깃
    T.put(open_x, ty, pal['shirt'][0]); T.put(open_x + 1, ty, pal['shirt'][1]); T.put(open_x + 1, ty + 1, pal['shirt'][2])
    # 허리띠
    by = ty + torso_h - 2
    for x in range(tx, tx + tw):
        if (x, by) in torso: T.put(x, by, pal['belt'][1])
        if H >= 36 and (x, by + 1) in torso: T.put(x, by + 1, pal['belt'][2])
    T.put(open_x, by, pal['gold'][0]); T.put(open_x + 1, by, pal['gold'][2])
    layers.append(T)
    # 앞팔
    FA = Layer()
    fx = tx + tw - aw + 1 - sw
    FA.fill(rrect(fx, ty + 1, aw, ah - 2, 1), pal['shirt'])
    for x in range(fx, fx + aw): FA.put(x, ty + ah - 4, pal['shirt'][2])       # 소맷부리
    FA.fill(rrect(fx, ty + ah - 3, aw, max(2, aw), 1), pal['skin']); layers.append(FA)
    # 머리
    HD = Layer()
    hw = round(hh * 1.12)
    hx0 = cx - hw // 2 + 1; hy0 = 1 + bob
    head = rrect(hx0, hy0, hw, hh, 3 if hh >= 13 else 2)
    head |= {(x, hy0 + hh) for x in range(hx0 + hw // 2, hx0 + hw - 3)}      # 턱선
    HD.fill(head, pal['skin'], 'round')
    # 얼굴: 오른쪽을 보는 3/4
    ey = hy0 + round(hh * 0.5)
    eh = 4 if hh >= 16 else 3
    ew = 2
    e1 = hx0 + round(hw * 0.52); e2 = hx0 + round(hw * 0.80)
    for ex, w_ in ((e1, ew), (e2, ew if hh >= 15 else ew - 0)):
        for yy in range(ey, ey + eh):
            for xx in range(ex, ex + w_): HD.put(xx, yy, pal['eye'])
        HD.put(ex, ey, pal['eyelite'])
        if eh >= 3: HD.put(ex + w_ - 1, ey + eh - 1, pal['iris'])
    # 눈썹
    for ex in (e1, e2): HD.put(ex, ey - 2, pal['brow']); HD.put(ex + 1, ey - 2, pal['brow'])
    # 볼, 입
    HD.put(e1 - 2, ey + eh, pal['blush']); HD.put(e1 - 1, ey + eh, pal['blush'])
    HD.put(e2 + 2, ey + eh - 1, pal['blush'])
    HD.put(e1 + (e2 - e1) // 2 + 1, ey + eh + 1, pal['mouth'])
    if hh >= 15: HD.put(e1 + (e2 - e1) // 2 + 2, ey + eh + 1, pal['mouth'])
    # 귀
    for yy in range(ey - 1, ey + 2): HD.put(hx0 + round(hw * 0.28), yy, pal['skin'][2])
    HD.put(hx0 + round(hw * 0.28) + 1, ey, pal['skin'][3])
    layers.append(HD)
    # 머리카락
    HR = Layer()
    hair = set()
    cap = ell(hx0 + hw / 2 - 0.5, hy0 + hh * 0.36, hw / 2 + 1.2, hh * 0.46)
    hair |= {(x, y) for (x, y) in cap if y <= hy0 + round(hh * 0.4)}
    hair |= {(x, y) for (x, y) in cap if x <= hx0 + round(hw * 0.3)}               # 뒷머리
    hair |= {(x, y) for x in range(hx0 - 1, hx0 + round(hw * 0.26)) for y in range(hy0 + 2, hy0 + round(hh * 0.8))}
    # 앞머리: 오른쪽 아래로 쓸린 뾰족한 덩어리
    base = hy0 + round(hh * 0.4)
    pattern = [2, 3, 1, 3, 2, 0, 2, 1]
    for i, x in enumerate(range(hx0 + round(hw * 0.32), hx0 + hw)):
        for y in range(base, base + pattern[i % len(pattern)]): hair.add((x, y))
    # 정수리 삐침, 뒤통수 삐침
    top = hy0 - 1
    for (x, y) in [(hx0 + hw // 2, top - 1), (hx0 + hw // 2 + 1, top - 2), (hx0 + hw // 2 + 2, top - 2),
                   (hx0 - 2, hy0 + 3), (hx0 - 3, hy0 + 4), (hx0 - 2, hy0 + 6), (hx0 - 3, hy0 + 7)]:
        hair.add((x, y))
    HR.fill(hair, pal['hair'], 'round')
    # 머리결 하이라이트와 가닥
    for x in range(hx0 + 2, hx0 + hw // 2 + 1): HR.put(x, hy0 + 1, pal['hair'][0])
    for x in range(hx0 + 3, hx0 + hw // 2 - 1, 3): HR.put(x, hy0 + 2, pal['hair'][0])
    for i, x in enumerate(range(hx0 + round(hw * 0.32), hx0 + hw, 3)):
        HR.put(x, base - 1, pal['hair'][2])
    layers.append(HR)
    return compose(layers, W, ground + 1)

if __name__ == '__main__':
    variants = [(32, 2.5), (32, 3), (40, 2.5), (40, 3)]
    Z = 8
    sheet = Image.new('RGBA', (1100, 2 * (44 * Z) + 60), (120, 104, 92, 255))
    for i, (H, n) in enumerate(variants):
        frames = [doyun(H, n, f) for f in range(4)]
        big = frames[0].resize((frames[0].width * Z, frames[0].height * Z), Image.NEAREST)
        gx = 10 + (i % 2) * 550; gy = 10 + (i // 2) * (44 * Z + 20)
        sheet.alpha_composite(big, (gx, gy + 44 * Z - big.height))
        for f in range(4):
            sm = frames[f].resize((frames[f].width * 3, frames[f].height * 3), Image.NEAREST)
            sheet.alpha_composite(sm, (gx + big.width + 6 + (f % 2) * (sm.width + 2), gy + 44 * Z - (2 - f // 2) * (sm.height + 4)))
    sheet.save('/home/claude/pix/doyun_test2.png'); print('ok')
