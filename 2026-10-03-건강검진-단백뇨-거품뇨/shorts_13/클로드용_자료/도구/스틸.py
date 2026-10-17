#!/usr/bin/env python3
"""완성 영상을 박마다 한 장씩 찍어 점검한다.

  python3 클로드용_자료/도구/스틸.py 완성_영상/모닝빈_12번.mp4                 → 영상 속 음악의 박을 직접 재서 박마다
  python3 클로드용_자료/도구/스틸.py 완성_영상/모닝빈_12번.mp4 클로드용_자료/작업/012/박자.json → 그 박자 파일의 시각으로
  python3 클로드용_자료/도구/스틸.py 완성_영상/모닝빈_12번.mp4 --간격 0.5       → 0.5초마다

클로드용_자료/작업/점검/모닝빈_12번/ 에 박마다 한 장(파일 이름 = 시각) + 모아보기.jpg(전부 한 장에) + 끝 정지 확인.
"""
import importlib.util
import json
import math
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True  # 클로드용_자료/도구/ 에 __pycache__ 를 남기지 않는다
from pathlib import Path

HERE = Path(__file__).resolve().parent


def tool():
    spec = importlib.util.spec_from_file_location("beat_tool", str(HERE / "박자.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ffbin(name):
    exe = shutil.which(name)
    if exe:
        return exe
    for d in ("/opt/homebrew/bin", "/usr/local/bin", str(Path.home() / ".local" / "bin")):
        if (Path(d) / name).exists():
            return str(Path(d) / name)
    sys.exit(f"{name} 를 찾지 못했습니다 — 클로드용_자료/자동설치.md")


def run(args):
    return subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    video = Path(sys.argv[1])
    ff, fp = ffbin("ffmpeg"), ffbin("ffprobe")
    dur = float(json.loads(run([fp, "-v", "error", "-show_entries", "format=duration", "-of", "json", str(video)]).stdout)["format"]["duration"])
    has_audio = "audio" in run([fp, "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(video)]).stdout

    times, how = [], ""
    if "--간격" in sys.argv:
        step = float(sys.argv[sys.argv.index("--간격") + 1])
        times, how = [round(i * step, 3) for i in range(int(dur / step) + 1)], f"{step}초마다"
    elif len(sys.argv) > 2 and sys.argv[2].endswith(".json"):
        data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        times, how = [b["t"] for b in data["beats"] if b["t"] < dur], f"{sys.argv[2]} 의 박"
    elif has_audio:
        data = tool().analyze(str(video))
        times, how = [b["t"] for b in data["beats"]], f"영상 속 음악에서 잰 박 ({data['bpm']} BPM)"
    if not times:
        times, how = [round(i * 0.5, 3) for i in range(int(dur / 0.5) + 1)], "0.5초마다 (소리 없음)"

    out = HERE.parent / "작업" / "점검" / video.stem      # 완성_영상 폴더를 어지럽히지 않게 클로드용_자료 안에
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True)
    for t in times:
        t2 = min(t + 0.05, max(0, dur - 0.05))  # 박이 떨어진 직후
        run([ff, "-v", "error", "-y", "-ss", f"{t2:.3f}", "-i", str(video), "-frames:v", "1", "-vf", "scale=640:-2",
             "-q:v", "3", str(out / f"{t:07.3f}s.jpg")])
    shots = sorted(out.glob("*s.jpg"))
    cols = 6
    rows = max(1, math.ceil(len(shots) / cols))
    lst = out / "_목록.txt"
    lst.write_text("".join(f"file '{p.name}'\nduration 1\n" for p in shots), encoding="utf-8")
    run([ff, "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-vf",
         f"scale=320:-2,tile={cols}x{rows}:padding=4:color=white", "-frames:v", "1", "-q:v", "3", str(out / "모아보기.jpg")])
    lst.unlink()

    # 끝 정지: 마지막 0.7초 안의 두 프레임 비교
    a, b = out / "_끝a.png", out / "_끝b.png"
    run([ff, "-v", "error", "-y", "-ss", f"{max(0, dur - 0.7):.3f}", "-i", str(video), "-frames:v", "1", str(a)])
    run([ff, "-v", "error", "-y", "-sseof", "-0.05", "-i", str(video), "-frames:v", "1", str(b)])
    psnr = run([ff, "-i", str(a), "-i", str(b), "-lavfi", "psnr", "-f", "null", "-"]).stderr
    m = re.search(r"average:(\S+)", psnr)
    for p in (a, b):
        p.unlink(missing_ok=True)
    still = m and (m.group(1) == "inf" or float(m.group(1)) > 40)

    print(f"{out} — {len(shots)}장 · {how}")
    print(f"모아보기: {out / '모아보기.jpg'}")
    print(f"끝 정지: {'예' if still else '아니오 — 마지막 0.7초에 아직 움직임이 있음'} (PSNR {m.group(1) if m else '?'})")


if __name__ == "__main__":
    main()
