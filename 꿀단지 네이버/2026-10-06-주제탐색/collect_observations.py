# -*- coding: utf-8 -*-
"""주제 탐색용 추가 관찰 수집기 (2026-10-06).

serp_collection의 자동완성/검색 화면 수집 함수를 그대로 호출하고
실제 응답 결과를 작업 폴더의 evidence 파일로 저장한다.
수집 실패(캡차·빈 결과)는 실패로 기록하며 판정을 만들지 않는다.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from serp_collection import autocomplete, fetch_serp  # noqa: E402

WORK = Path(__file__).resolve().parent
EVID = WORK / "evidence"
EVID.mkdir(exist_ok=True)


def now():
    return datetime.now().astimezone().isoformat()


def save(name, data):
    path = EVID / name
    if path.exists():
        raise SystemExit(f"기존 근거 파일을 덮어쓰지 않습니다: {path}")
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def main():
    mode = sys.argv[1]
    label = sys.argv[2]
    queries = sys.argv[3:]
    out = {"mode": mode, "collected_at": now(), "results": []}
    for q in queries:
        if mode == "ac":
            for ch in ("naver", "google"):
                r = autocomplete(ch, q)
                out["results"].append(dict(channel=ch, seed=q, observed_at=now(), **r))
        elif mode in ("naver", "google"):
            r = fetch_serp(mode, q)
            out["results"].append(dict(channel=mode, query=q, **r))
    path = save(f"{label}.json", out)
    for r in out["results"]:
        if mode == "ac":
            print(r["channel"], "|", r["seed"], "|", r["status"], "|", r["items"][:8])
        else:
            print(r["channel"], "|", r["query"], "|", r["collection_status"], "|", r.get("error"),
                  "| docs", len(r["top_docs"]))
            for d in r["top_docs"][:6]:
                print("   ", d.get("rank"), d.get("title", "")[:60], "|", d.get("url", "")[:90])
    print("saved", path.name)


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    main()
