#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""꿀단지 (KKULDANJI) -> 공용 AI 전용 크롬 CDP (D:\\작업\\ai_chrome_cdp.py) 브릿지"""
import runpy
import sys
from pathlib import Path

SHARED_SCRIPT = Path(r"D:\작업\ai_chrome_cdp.py")
if __name__ == "__main__":
    sys.path.insert(0, str(SHARED_SCRIPT.parent))
    runpy.run_path(str(SHARED_SCRIPT), run_name="__main__")
