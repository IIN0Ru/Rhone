from PIL import Image
from char2 import rect, rrect, Layer, compose, hx, PAL_DOYUN
from heads import HEAD11, HEAD13, HEAD16, head_pixels

HEADS = {11: HEAD11, 13: HEAD13, 16: HEAD16}

def doyun(H=32, heads=2.5, frame=0, pal=PAL_DOYUN):
    hh = round(H / heads)
    key = min(HEADS, key=lambda k: abs(k - hh))
    hp, hw, hhh = head_pixels(HEADS[key])
    W = hw + 12
    ground = H + 3
    bob = 1 if frame in (1, 3) else 0
    head_y = 0 + bob
    neck_y = head_y + hhh - 3                     # 몸통이 턱 아래로 살짝 들어가게
    body = ground - neck_y
    torso_h = round(body * (0.48 if heads < 2.8 else 0.43))
    tw = max(8, round(hw * 0.52))
    cx = 6 + round(hw * 0.55)                     # 얼굴 중심 아래
    tx = cx - tw // 2
    ty = neck_y
    leg_top = ty + torso_h - 2
    lw = max(3, round(tw * 0.42))
    boot_h = max(2, round((ground - leg_top) * 0.3))
    step = {0: 2, 1: 0, 2: -2, 3: 0}[frame]
    dark = lambda r: (r[1], r[2], r[3], r[3])
    layers = []
    def leg(x, lift, rp, rb):
        L = Layer()
        L.fill(rect(x, leg_top, lw, ground - leg_top - boot_h - lift), rp)
        L.fill(rrect(x, ground - boot_h - lift, lw + 1, boot_h, 1), rb)
        for xx in range(x, x + lw + 1): L.put(xx, ground - lift - 1, rb[3])
        return L
    layers.append(leg(tx + 1 - step, 1 if frame == 0 else 0, dark(pal['pants']), dark(pal['boots'])))
    aw = 3 if H < 36 else 4
    ah = torso_h - 1
    sw = -step // 2
    BA = Layer(); BA.fill(rrect(tx - aw + 2 + sw, ty + 1, aw, ah - 2, 1), dark(pal['shirt']))
    BA.fill(rrect(tx - aw + 2 + sw, ty + ah - 3, aw, 3, 1), dark(pal['skin'])); layers.append(BA)
    layers.append(leg(tx + tw - lw - 1 + step, 1 if frame == 2 else 0, pal['pants'], pal['boots']))
    T = Layer()
    torso = rrect(tx, ty, tw, torso_h, 2)
    T.fill(torso, pal['shirt'], 'round')
    open_x = tx + tw - 4
    vest = {(x, y) for (x, y) in torso if not (open_x <= x <= open_x + 1 and y < ty + torso_h - 2) and x < tx + tw - 1}
    T.fill(vest, pal['vest'], 'round')
    for y in range(ty + 3, ty + torso_h - 2, 2): T.put(open_x - 1, y, pal['gold'][1])
    by = ty + torso_h - 2
    for x in range(tx, tx + tw):
        if (x, by) in torso: T.put(x, by, pal['belt'][1])
        if H >= 36 and (x, by + 1) in torso: T.put(x, by + 1, pal['belt'][2])
    T.put(open_x, by, pal['gold'][0]); T.put(open_x + 1, by, pal['gold'][2])
    # 주머니(40px만)
    if H >= 36:
        for x in range(tx + 2, tx + 5): T.put(x, by - 3, pal['vest'][3])
    layers.append(T)
    FA = Layer()
    fx = tx + tw - aw + 1 - sw
    FA.fill(rrect(fx, ty + 2, aw, ah - 3, 1), pal['shirt'])
    for x in range(fx, fx + aw): FA.put(x, ty + ah - 4, pal['shirt'][2])
    FA.fill(rrect(fx, ty + ah - 3, aw, 3, 1), pal['skin']); layers.append(FA)
    im = compose(layers, W, ground + 1)
    # 손으로 찍은 머리 올리기
    for (x, y), c in hp.items():
        X, Y = x + 5, y + head_y
        if 0 <= X < W and 0 <= Y < ground + 1: im.putpixel((X, Y), hx(c))
    return im

def preview(path, bg=(150, 132, 116, 255)):
    variants = [(32, 2.5), (32, 3), (40, 2.5), (40, 3)]
    Z = 8
    sheet = Image.new('RGBA', (1180, 2 * (46 * Z) + 40), bg)
    for i, (H, n) in enumerate(variants):
        fr = [doyun(H, n, f) for f in range(4)]
        big = fr[0].resize((fr[0].width * Z, fr[0].height * Z), Image.NEAREST)
        gx = 10 + (i % 2) * 590; gy = 10 + (i // 2) * (46 * Z + 10)
        sheet.alpha_composite(big, (gx, gy + 46 * Z - big.height))
        for f in range(4):
            sm = fr[f].resize((fr[f].width * 3, fr[f].height * 3), Image.NEAREST)
            sheet.alpha_composite(sm, (gx + big.width + 6 + (f % 2) * (sm.width + 2), gy + 46 * Z - (2 - f // 2) * (sm.height + 4)))
    sheet.save(path)

if __name__ == '__main__':
    preview('/home/claude/pix/doyun_test3.png'); print('ok')
