"""Legacy command name for the evidence-led topic agent.

No seeds/category rotation are silently invented. With no seed the agent uses
GSC observations when available, then continues public search as instructed.
"""
import argparse
from datetime import datetime
from pathlib import Path
import sys
try:
    from .topic_opportunity import prepare, ROOT, KST
except ImportError:
    from topic_opportunity import prepare, ROOT, KST


def build_dynamic_candidates_from_queries(seed, suggestions):
    return [dict(id=i, title=q, keyword=q, status='additional_research',
                 tier='탐색 후보', serp_note='수집 표현; 경쟁·검색량 미측정')
            for i, q in enumerate(dict.fromkeys(suggestions or [seed]), 1)]


def run_topic_suggestion(user_seed=None, work_dir=None, offline=False):
    work = Path(work_dir) if work_dir else ROOT / '꿀단지 네이버' / (datetime.now(KST).strftime('%Y-%m-%d-%H%M%S') + '-주제탐색')
    result = prepare(work, [user_seed] if user_seed else [], use_gsc=not offline, collect=not offline)
    print(f"후보 자료 {len(result['candidates'])}개: {work}")
    print('추천은 아직 없음. skills/topic-opportunity/SKILL.md에 따라 공개 검색과 상대 비교를 계속하세요.')
    return result


if __name__ == '__main__':
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('seed', nargs='?')
    parser.add_argument('--work-dir', type=Path)
    parser.add_argument('--offline', action='store_true')
    args = parser.parse_args()
    try:
        run_topic_suggestion(args.seed, args.work_dir, args.offline)
    except (ValueError, OSError) as exc:
        parser.exit(2, f'보완 필요: {exc}\n')
