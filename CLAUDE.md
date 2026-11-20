# CLAUDE.md — 로운(Rhone) 작업 지침

이 저장소에서 일하는 AI 세션은 **이 파일 → docs/DEMO_SPEC.md → docs/DECISIONS.md → docs/DEVLOG.md 마지막 항목** 순서로 읽고 시작한다. 데모 제작은 `docs/DEMO_SPEC.md`, 그림 생성은 `docs/ART_SPEC.md`, 전체 이야기는 `docs/STORY.md`, 세계관 요약은 `docs/WORLD.md`가 기준이다.

## 사용자와 일하는 방식

- **항상 한국어**로 답한다.
- 사용자는 **솔직한 조언자**를 원한다. 위로·칭찬보다 문제점과 우선순위를 먼저 말한다. 결과물이 별로면 별로라고 말한다.
- **코드를 짜기 전에 애매한 건 먼저 묻는다.** 단, 사용자가 답하지 않고 넘어간 질문을 다시 재촉하지 않는다(다른 게 더 급하다는 뜻).
- 선택지를 줄 때는 **추천안과 그 이유**를 같이 준다. 시안(눈으로 보는 비교)을 좋아한다 — 말로 설명하기보다 만들어서 보여준다.
- 사용자가 내린 결정은 [docs/DECISIONS.md](docs/DECISIONS.md)에 기록되어 있다. **확정된 결정을 임의로 뒤집지 않는다.** 바꾸자고 제안할 수는 있다.

## 프로젝트 핵심 (자세한 건 docs/)

- **도시 = 스타듀밸리식 정면 내려다보기**, **던전·전투 = 옆모습 횡스크롤** + 자동 전투(슬롯바운드식 연출) + 파티 고용 RPG. 최종 목표 **Steam + App Store**.
- 플레이어 남성 고정. 고향 친구 **유진**(여) + 고용 동료 2명 (파티 최대 4명).
- 던전: 들어가면 **층을 끝낼 때까지 자동 전진, 중간 탈출 없음.** 사망 없음 → **기절**(전리품 전부 잃음 + 10일 경과 + HP1 + 동료별 호감도 하락).
- 저장은 **자유 저장**(던전 안만 불가).
- UI는 **스타듀밸리식**. 그래픽 배율 **×4**. 캐릭터는 **32×32 캔버스(인물 키 약 29px)**, 기준 = 도윤 P3 (`assets/pixellab/final/doyun_idle_base.png`).

## 코드 구조 (prototype/index.html, 바닐라 JS + Canvas 2D)

- 논리 해상도 **960×600**, 지면 `GY=496`, 픽셀 배율 `PX=4`. 무대(#stage)를 화면에 맞춰 `transform: scale`.
- 주요 상태 객체 `G` (phase, scene, day, gold, player, party, lodging, battle, log …).
- 씬: `town`, 실내(`tavern`,`inn`,`shop`,`lodge`,`stable`,`train`), 던전(`d1`,`d2`,`d3`). 폭은 `SC[scene].w` (월드 좌표 = 원본 픽셀 × 4).
- 배경 그림은 `BGART[scene]`(art9.js) → `drawArt(key)`. 캐릭터는 `SPRITES[key].idle/run` → `sprDraw()`. 스프라이트가 없으면 이모지로 폴백.
- 대화·선택은 전부 `await modal(html, buttons)` (Promise). 대사는 `talkHtml(u, line)` 로 감싸면 초상화가 붙는다.
- UI 갱신은 `renderUI()` (HUD/토스트/메뉴/전투 패널/터치 버튼).
- 저장: `localStorage['sanggyeong_saves_v1']` 3슬롯 (`snapshot()` / `restore()`). 키 이름은 호환성 때문에 옛 이름 유지.

## 작업 규칙

- 게임 코드를 고치면 **반드시 `tools/test/` 봇을 돌려 에러 0을 확인**하고, 바뀐 화면은 스크린샷으로 직접 본다.
  ```bash
  pip install playwright && python3 -m playwright install chromium
  python3 tools/test/bot9.py      # 랜덤 플레이 (에러 수 출력)
  python3 tools/test/t9.py        # 던전 전투 스크린샷
  ```
  스크린샷은 `tools/test/out/`에 저장된다. 시스템 크롬을 쓰려면 `CHROME_PATH=/경로/chrome` 환경변수를 준다.
- 새 버전을 만들면 [docs/DEVLOG.md](docs/DEVLOG.md)에 한 항목 추가하고, 새 결정은 DECISIONS.md에 추가한다.
- 에셋을 추가하면 [docs/CREDITS.md](docs/CREDITS.md)에 출처·라이선스를 적는다. **라이선스가 불분명한 에셋은 쓰지 않는다.**
- 커밋 메시지는 한국어 OK. 큰 변경은 브랜치 → PR.

## 지금 하던 일 / 다음 할 일

[docs/ROADMAP.md](docs/ROADMAP.md)의 "지금 단계" 참고. 2026-11-17 기준: 도윤·유진(기준·걷기·공격) 완료, `assets/pixellab/final/`. 다음은 **파티원(바르크·연소하·소소·기사) → 몬스터**. 새 캐릭터는 도윤 P3를 `edit_image_pixen`으로 변환하는 방식이 화풍 유지에 가장 좋았다.
