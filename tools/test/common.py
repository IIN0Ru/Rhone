"""테스트 공통 설정. 크롬 경로는 CHROME_PATH 환경변수(없으면 Playwright 기본 Chromium),
스크린샷은 tools/test/out/ 에 저장한다."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
URL = (ROOT / 'prototype' / 'index.html').as_uri()
OUT = Path(__file__).resolve().parent / 'out'
OUT.mkdir(exist_ok=True)


def launch_args():
    kw = {'args': ['--no-sandbox']}
    if os.environ.get('CHROME_PATH'):
        kw['executable_path'] = os.environ['CHROME_PATH']
    return kw


def shot(name: str) -> str:
    return str(OUT / name)
