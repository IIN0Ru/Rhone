# 아트 파이프라인

## 현재 (프로토타입 v9)
- 캐릭터·몬스터: **0x72 DungeonTileset II (CC0)** 원본 + 색 바꾼 변형(farmer, kid, barkeep, innkeep, shopkeep, goblin_archer)
- 늑대, 거리, 실내 6곳, 던전 3층: `tools/pixel/*.py` 로 **코드로 직접 찍음** (PIL)
- 화면 배율 ×4, 캐릭터 실제 크기 약 16×20px
- UI 아이콘: 0x72 (코인, 하트, 물약, 상자), 폰트: 갈무리11 (OFL)

**이건 임시다.** 정식 아트는 아래 PixelLab 규격으로 전부 교체한다.

## 정식 규격 (2026-11-17 1차안 — **아래 표는 폐기, 최신 규격은 DECISIONS: 32×32 캔버스·×4**)
| 항목 | 규격 |
|---|---|
| 캐릭터 캔버스 | **32×40**, 발이 맨 아래 줄 |
| 시점 | **측면, 오른쪽 보기** (왼쪽은 코드에서 좌우 반전) |
| 화면 배율 | ×3 (예정) |
| 외곽선 | 단색 진한 외곽선 |
| 광원 | 왼쪽 위 |
| 팔레트 | 캐릭터당 12~16색 내외, 노을 배경과 어울리는 따뜻한 톤 |
| 무기 | 몸과 분리 (허리에 차는 형태) — 장비 교체 대비 |
| 초상화 | 64×64, 표정 4종 |
| 아이콘 | 32×32 |

## PixelLab 사용법

### 연결 방식
1. 웹(pixellab.ai)에서 생성 → 투명 PNG로 받아 이 저장소 `assets/` 에 넣기 (가장 확실)
2. MCP: 서버 `https://api.pixellab.ai/mcp`, Bearer 토큰 인증. Claude Code: 
   `claude mcp add pixellab https://api.pixellab.ai/mcp -t http -H "Authorization: Bearer <TOKEN>"`
   (claude.ai 커스텀 커넥터는 OAuth 방식이라 동작 여부 미확인)
   - ⚠️ 토큰을 채팅·커밋에 절대 넣지 않는다.
- 요금: Tier 1 $12/월로 시작, 400×400·Instant Character 등이 필요하면 Tier 2.

### 작업 순서
도윤(스타일 기준) → 파티원 → 애니메이션 → 초상화 → 몬스터 → 아이콘 → 배경. 
**스타일 기준 이미지 1장을 모든 생성의 style reference로 쓴다.**

### 도윤 프롬프트 (기본형)
```
pixel art game sprite, side view facing right, full body standing idle,
young male swordsman from the countryside, messy brown hair,
cream linen shirt, brown leather vest, blue trousers, brown boots,
short sword in scabbard at left hip, friendly determined face,
dark outline, light from top-left, limited palette, transparent background
```
negative: `front view, top-down, background, ground shadow, text, blurry, anti-aliasing`

설정: 캔버스 32×40 · view side · direction east · outline single color · shading basic~medium · detail medium · 투명 배경.
측면이 잘 안 나오면 8방향 Pro 도구의 side view에서 east 프레임만 사용.

### 고르는 기준
1. 실루엣만으로 사람으로 읽히는가
2. 얼굴·몸 방향이 모두 오른쪽인가
3. 발이 캔버스 맨 아래인가
4. 색 수가 과하지 않은가
5. 실제 배율(×3)에서 얼굴·조끼가 구분되는가
→ 후보는 반드시 **게임 화면에 세워서** 비교한다.

### 파일 규칙
- 투명 PNG, 애니메이션은 **가로 1줄 스프라이트시트**
- 이름: `<캐릭터>_<동작>_<프레임수>f.png` 예) `doyun_walk_6f.png`, `yujin_portrait_happy.png`
- 같은 캐릭터의 모든 프레임은 같은 캔버스 크기
- 원본은 `assets/`, 게임에 넣는 묶음(base64 JS 등)은 빌드 단계에서 생성

### 클라우드 세션에서 PNG 받는 법 (2026-11-17 확인)
claude.ai 커넥터(PixelLab)는 연결됨. 하지만 클라우드 작업 공간에서는 `api.pixellab.ai`·`backblaze.pixellab.ai` 다운로드가 **막혀 있다.** 우회:
1. `pixelart_workbench(["inspect", "character:<id>:east"])` → 결과 이미지가 3배 확대 미리보기 PNG로 `/tmp/claude-tool-results/…`에 저장됨
2. `python3 tools/pixellab/unpreview.py <미리보기.png> 48 48 <출력.png>` → 원본 픽셀로 정확히 복원 (블록 균일성·색 수 검증 출력)
- 체험판(Tier 0)은 **동시 생성 1개** → 순서대로 돌릴 것. v3 텍스트 생성은 16~90px에서 2회.
- 로컬 Claude Code에서는 `export_asset` 링크로 바로 받으면 된다.

### 도윤 1차 후보 (2026-11-17)
v3 · view side · 48px · east 방향. `assets/pixellab/candidates/` (A: 디테일↑ 48색, B: 중간 54색, C: 플랫·외곽선 강함 38색). 실제 인물 높이 약 45px → 규격 32×40보다 큼. 비교 이미지 `doyun_candidates.png`.

### 도윤 2차: v1 기반 (2026-11-17)
`now_variants.png`(now→v1~v3 늘리기) → v1 채택. v1을 32×32로 패딩해 `create_image_pixflux` img2img(1회)로 재디자인: strength 150 = pl1(기획 의상 반영, 비율 유지), 260 = pl2(거의 안 바뀜), 110 = pl3(비율 붕괴). 비교 `v1_pixellab.png`.

### 필요한 아트 목록 (2026-11-17, 무기 분리 기준)
| 대상 | 몸(대기·걷기) | 무기 오버레이 | 공격 동작 |
|---|---|---|---|
| 도윤 | ✅ 1벌 (현재 칼이 몸에 붙어 있음 → 칼 지운 몸 필요) | 칼·활·지팡이·방패 | 베기 ✅ / 활 / 마법 / 방패 |
| 유진 | ⚠️ 현재 그림은 검사 → 칼 지운 몸으로 재사용 | 활·지팡이 | 활 / 마법 |
| 바르크·기사 | 필요 | 방패(+대안 무기 1) | 방패 |
| 연소하 | 필요 | 칼(+대안 1) | 베기 |
| 소소 | 필요 | 투척(+대안 1) | 던지기 |
공격 동작은 무기 종류별로 캐릭터마다 필요(무기 분리해도 몸 자세가 다름). 우선순위: 데모 첫 판에 보이는 것부터 — 유진 궁수/마법사 → 바르크 → 연소하 → 소소 → 기사 → 몬스터.

## 수작업 보정
AI 결과물은 손 모양, 프레임 간 픽셀 흔들림, 팔레트 오염이 생긴다. 에셋당 5~15분 보정 예상 (PixelLab 웹 에디터/Aseprite).

## 코드 도트 스크립트 (tools/pixel)
`pixlib.py`(공통 도형·벽·창문·간판 함수) 위에 `street2.py`(거리), `interiors.py`(여관·마구간), `interiors2.py`(술집·객잔·잡화점·수련장), `dungeon.py`(던전 3층 + 늑대). `tools/pixel/` 안에서 실행하면 `assets/source/`에 저장되고, 다른 곳에 저장하려면 `RHONE_PIX_OUT` 환경변수를 준다(`outpath.py`). 폐기한 도윤 코드 도트 스크립트(char2·char3·heads)는 삭제했다. PixelLab 전환 후에는 참고용.
