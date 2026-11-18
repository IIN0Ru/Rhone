# 로운 (Rhone)

> 파티원을 **돈으로 고용**하고, 숨겨진 **특성**과 **호감도**에 휘둘리며 던전을 공략하는 2D 횡스크롤 RPG.

- **장르**: 2D 횡스크롤 · 파티 고용 · 자동 전투(슬롯바운드식 연출) RPG
- **최종 목표**: **Steam** 출시 + **App Store(iOS)** 출시 (Google Play는 같은 빌드로 추가 가능)
- **개발 형태**: 1인 개발 (기획·결정: 이상인 / 코드·도트 대부분: Claude)
- **현재 단계**: 웹 프로토타입 v9 (게임 루프 검증 + 도트 그래픽 1차 완료)

---

## 한 줄 컨셉

동료는 공짜가 아니다. 술집·객잔·뒷골목·던전에서 파티원을 고용하지만, 그들은 **명령을 안 듣고, 도망가고, 배신하고, 가끔 아군을 친다.** 숙소의 질, 선물, 함께 깬 던전이 호감도를 바꾸고, 호감도가 전투를 바꾼다.

## 바로 해보기

```bash
# 아무 정적 서버로 prototype/ 폴더를 열면 된다
cd prototype && python3 -m http.server 8000
# → http://localhost:8000
```

조작: `← →` 이동 · `Space` 대화/공격 · `↑↓` 선택지 · `1` 회복약 · `2` 선물 · `Esc` 메뉴(파티/일지/저장)

## 저장소 구조

```
prototype/        현재 플레이 가능한 웹 프로토타입 (단일 HTML + 에셋 JS)
  index.html      게임 전체 코드 (v9)
  art9.js         스프라이트·배경 PNG(base64) 묶음 — tools/pixel 로 생성
  ui7.js          UI 아이콘(코인, 하트, 물약 등)
  Galmuri11.woff2 한글 도트 폰트 (OFL)
assets/source/    배경·몬스터 원본 PNG (1배율 픽셀)
tools/pixel/      배경·실내·던전·늑대를 코드로 찍는 Python(PIL) 스크립트
tools/test/       Playwright 자동 플레이 봇 / 스크린샷 테스트
docs/             기획·결정·로드맵·아트 파이프라인·개발 일지
CLAUDE.md         AI 세션용 작업 지침 (새 세션은 이것부터 읽기)
```

## 문서

| 문서 | 내용 |
|---|---|
| [docs/GAME_DESIGN.md](docs/GAME_DESIGN.md) | 게임 기획 전체 (시스템, 캐릭터, 전투, 던전 규칙) |
| [docs/DECISIONS.md](docs/DECISIONS.md) | 확정된 결정과 그 이유 — **뒤집기 전에 꼭 확인** |
| [docs/ROADMAP.md](docs/ROADMAP.md) | 프로토타입 → Steam / App Store 출시까지의 단계 |
| [docs/ART_PIPELINE.md](docs/ART_PIPELINE.md) | 도트 규격, PixelLab 사용법, 파일 규칙 |
| [docs/DEVLOG.md](docs/DEVLOG.md) | v1~v9 변경 내역과 플레이테스트 피드백 |
| [docs/CREDITS.md](docs/CREDITS.md) | 에셋·폰트 라이선스, AI 사용 고지 |

## 현재 상태 요약 (2026-11-17)

- ✅ 마을(횡스크롤) · 실내 6곳 · 던전 3층 · 자동 전투 · 고용/특성/호감도 · 기절 페널티 · 자유 저장(3슬롯) · 엔딩
- ✅ 스타듀밸리식 UI (화면 안 HUD, 하단 대화창 + 초상화, Esc 메뉴, 토스트 알림)
- ⚠️ 캐릭터는 무료 에셋(0x72, CC0) 임시 사용 → **PixelLab으로 교체 예정 (기준 32×40)**
- ⚠️ 사운드 없음, 초상화가 16px 확대본이라 거침
- ⬜ 엔진/패키징 결정 (Steam·iOS 빌드 방식) — [ROADMAP](docs/ROADMAP.md) 참고
