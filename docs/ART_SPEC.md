# 아트 사양서 — PixelLab 생성용

> 프롬프트를 그대로 복사해서 쓴다. 생성 후 `assets/pixellab/final/`에 규칙대로 저장 → `tools/pixellab/build_art_pl.py`.

## 공통 규격 ✅
- 캐릭터: **32×32 캔버스, 인물 키 약 29px**. 스타일 기준 = `assets/pixellab/final/doyun_idle_base.png` (도윤 P3)
- 새 캐릭터 만드는 법: 도윤 P3를 `edit_image_pixen`으로 변환 ("turn this character into a different person in the exact same art style..."), 1회
- 무기는 몸과 분리: `assets/pixellab/weapons/` 를 겹쳐 씀. 공격 동작만 `animate_image`로 생성(1회, 8프레임)
- 도시 배경: 시안 B (`assets/pixellab/candidates/town/plazaB.png`) 그림체, `create_image_pixflux` view=high top-down, 240×152
- 체험판: 동시 생성 1개, 클라우드 세션은 다운로드가 막혀 `pixelart_workbench inspect` → `tools/pixellab/unpreview.py`로 받는다 (ART_PIPELINE.md)

## 에셋 목록 ⬜ (설정 확정 후 채움)
