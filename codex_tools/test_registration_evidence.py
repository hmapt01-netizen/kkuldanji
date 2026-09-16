"""Read-only integration checks against a temporary copy of real evidence."""
import contextlib, io, shutil, tempfile, unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
import step_guard

class EvidenceIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.work=Path(self.tmp.name)/'work'
        source=Path(__file__).resolve().parents[1]/'꿀단지 네이버/2026-09-15-중성지방-음주-재검'
        shutil.copytree(source,self.work,ignore=shutil.ignore_patterns('images','image_originals','registration_backup','__pycache__'))
    def tearDown(self):self.tmp.cleanup()
    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):return step_guard.verify_research_facts(str(self.work))
    def test_original_separate_reports_pass(self):self.assertTrue(self.check())
    def test_tampered_evidence_blocked(self):
        import json
        data=json.loads((self.work/'codex_target.json').read_text(encoding='utf-8'))
        p=self.work/data['channels']['naver']['evidence_file']
        p.write_text('{}',encoding='utf-8')
        with self.assertRaises(ValueError):self.check()
    def test_target_changed_blocked(self):
        import json
        p=self.work/'codex_target.json';data=json.loads(p.read_text(encoding='utf-8'))
        data['channels']['naver']['evidence_file']='data/last_serp_audit.json'
        p.write_text(json.dumps(data),encoding='utf-8')
        with self.assertRaises(ValueError):self.check()

if __name__=='__main__':unittest.main()
