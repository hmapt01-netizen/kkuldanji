from pathlib import Path
import hashlib, json

R = Path(__file__).resolve().parents[2]
W = Path(__file__).resolve().parent
paths = list((R/'kkuldanji_web').glob('*.html')) + list((R/'kkuldanji_web/templates').glob('*.html')) + [R/'tools/build_site.py', R/'data/posts_db.json', R/'AGENTS.md', R/'GEMINI.md']
manifest = {}
for p in paths:
    data = p.read_bytes()
    dest = W/'before'/p.relative_to(R)
    if not dest.exists():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    manifest[str(p.relative_to(R))] = hashlib.sha256(dest.read_bytes()).hexdigest()
(W/'before_manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print('Backed up', len(manifest), 'source files')
