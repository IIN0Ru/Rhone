"""PixelLab 워크벤치 미리보기(3배 확대 + 상단 라벨 + 단색 배경)를 원본 RGBA 스프라이트로 복원."""
import sys
from PIL import Image
src, w, h, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
im = Image.open(src).convert('RGBA')
S = im.width // w
top = im.height - h * S
bg = im.getpixel((im.width - 1, im.height - 1))
res = Image.new('RGBA', (w, h))
bad = 0
for y in range(h):
    for x in range(w):
        block = {im.getpixel((x*S+i, top+y*S+j)) for i in range(S) for j in range(S)}
        if len(block) != 1: bad += 1
        c = im.getpixel((x*S + S//2, top + y*S + S//2))
        res.putpixel((x, y), (0, 0, 0, 0) if c == bg else c)
res.save(out)
print(f'scale={S} top={top} bg={bg} nonuniform_blocks={bad} bbox={res.getbbox()}')
