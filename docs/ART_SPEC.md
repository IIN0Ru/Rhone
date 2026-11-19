# 아트 사양서 — PixelLab 생성용

> 프롬프트를 그대로 복사해서 쓴다. 생성 후 `assets/pixellab/final/`에 규칙대로 저장 → `tools/pixellab/build_art_pl.py`.

## 공통 규격 ✅
- 캐릭터: **32×32 캔버스, 인물 키 약 29px**. 스타일 기준 = `assets/pixellab/final/doyun_idle_base.png` (도윤 P3)
- 새 캐릭터 만드는 법: 도윤 P3를 `edit_image_pixen`으로 변환 ("turn this character into a different person in the exact same art style..."), 1회
- 무기는 몸과 분리: `assets/pixellab/weapons/` 를 겹쳐 씀. 공격 동작만 `animate_image`로 생성(1회, 8프레임)
- 도시 배경: 시안 B (`assets/pixellab/candidates/town/plazaB.png`) 그림체, `create_image_pixflux` view=high top-down, 240×152
- 체험판: 동시 생성 1개, 클라우드 세션은 다운로드가 막혀 `pixelart_workbench inspect` → `tools/pixellab/unpreview.py`로 받는다 (ART_PIPELINE.md)

## 도구 분담 (2026-11-20)
| 도구 | 맡는 것 | 이유 |
|---|---|---|
| **PixelLab** | 캐릭터(동료·용병·몬스터), 애니메이션(걷기·공격), 캐릭터 방향 전환 | 도윤 P3를 기준으로 같은 화풍 변환은 여기서만 가능 |
| **Pixel Factory** (사용자 PC, Codex 계정) | 아이템 아이콘(무기 20종·물약·선물), 도시·던전 배경, UI 요소, 이벤트 그림 | 정확한 W×H 칸·색 수 제한, PixelLab 횟수 절약 |

### Pixel Factory 사용 규칙
- 팔레트는 **"로운 · 32색"**(`assets/rhone_palette.json`)을 쓴다 — 도윤·유진·바르크·도시 시안 B·무기 시트에서 추출. 사용자에게 준 `pixel-factory-1.0.0-rhone.zip`에 버튼으로 들어 있음.
- 캐릭터·아이템 스타일은 투명 배경 자동. 배경(scene)은 불투명.
- 프롬프트 공통 꼬리말: `16-bit pixel art, clean dark outlines, warm palette, readable silhouette`
- 크기: 아이템 아이콘 16×16 또는 24×24 / 무기 오버레이 32×32(몸에 겹칠 위치 고려) / 도시 배경 240×152 / 던전 배경 960~1600×150 (넓은 건 나눠서)
- 결과는 "원본 크기 PNG"로 받아서 `assets/pixelfactory/`에 저장, 출처는 CREDITS에 "Pixel Factory(Codex 이미지 생성)"로 기록.

로운 팔레트 32색: `#0d0619 #0b0921 #251f23 #311c35 #243631 #42242a #313852 #653936 #773827 #404a60 #544552 #467539 #4f4b5f #7b4e41 #675967 #835c49 #b93f44 #9f5c4a #517489 #85a62f #7c6d75 #837273 #bc855a #6f8ca2 #70a0af #ad9a86 #cc9276 #b4a08d #87bcb8 #e1c3a5 #f3e6ca #f9eedf`

## 에셋 목록 ⬜ (설정 확정 후 채움)
