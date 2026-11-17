"""도트 스크립트 공통 출력 경로.
기본값은 저장소의 assets/source/. 환경변수 RHONE_PIX_OUT 으로 바꿀 수 있다."""
import os
from pathlib import Path

OUT_DIR = Path(os.environ.get('RHONE_PIX_OUT', Path(__file__).resolve().parents[2] / 'assets' / 'source'))
OUT_DIR.mkdir(parents=True, exist_ok=True)


def out(name: str) -> str:
    return str(OUT_DIR / name)
