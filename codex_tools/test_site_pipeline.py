import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import site_pipeline as s
import workflow_guard as g

class SitePipelineTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.work=self.root/'work'; self.work.mkdir()
        self.web=self.root/'web'
        self.patchers=[patch.object(s,'ROOT',self.root),patch.object(s,'WEB',self.web)]
        for p in self.patchers:p.start()
        self.data={'slug':'article.html','title':'Selected title','bodyHtml':'Body','isEditorPick':False}
        (self.root/'data').mkdir()
        self.save(self.root/'data/posts_db.json',[self.data])
        self.save(self.work/'post_data.json',self.data)
        paths=s.site_files(self.data)
        for p in paths:p.parent.mkdir(parents=True,exist_ok=True);p.write_text('content')
        (self.work/'images').mkdir();(self.work/'images/post01.jpg').write_bytes(b'image')
        (self.work/'site_audit.log').write_text('passed')
        self.report={'input_sha256':s.digest(self.work/'post_data.json'),'outputs':{str(p.relative_to(self.root)):s.digest(p) for p in paths},'images':{'post01.jpg':s.digest(self.work/'images/post01.jpg')},'audit_exit':0,'audit_sha256':s.digest(self.work/'site_audit.log')}
        self.save(self.work/s.REPORT,self.report)
    def save(self,p,v):p.write_text(json.dumps(v),encoding='utf-8')
    def tearDown(self):
        for p in reversed(self.patchers):p.stop()
        self.tmp.cleanup()
    def test_registered_site_passes(self):self.assertEqual(s.verify(self.work),s.REPORT)
    def test_preview_only_blocked(self):
        (self.work/s.REPORT).unlink()
        with self.assertRaises(OSError):s.verify(self.work)
    def test_missing_real_page_blocked(self):
        s.site_files(self.data)[0].unlink()
        with self.assertRaises(ValueError):s.verify(self.work)
    def test_changed_input_blocked(self):
        self.save(self.work/'post_data.json',dict(self.data,title='changed'))
        with self.assertRaises(ValueError):s.verify(self.work)
    def test_changed_database_blocked(self):
        self.save(self.root/'data/posts_db.json',[])
        with self.assertRaises(ValueError):s.verify(self.work)
    def test_changed_image_blocked(self):
        (self.work/'images/post01.jpg').write_bytes(b'new')
        with self.assertRaises(ValueError):s.verify(self.work)
    def test_failed_audit_blocked(self):
        self.report['audit_exit']=1;self.save(self.work/s.REPORT,self.report)
        with self.assertRaises(ValueError):s.verify(self.work)
    def test_validation_record_cannot_skip_registration(self):
        (self.work/s.REPORT).unlink()
        with patch.object(g,'state_of',return_value={}),patch.object(g,'next_step',return_value=('validation','')):
            with self.assertRaises(OSError):g.record(self.work,'validation',[],'preview only')
    def test_draft_without_site_input_blocked(self):
        (self.work/'post_data.json').unlink()
        with patch.object(g,'state_of',return_value={}),patch.object(g,'next_step',return_value=('draft','')):
            with self.assertRaises(ValueError):g.record(self.work,'draft',[],'draft')

if __name__=='__main__':unittest.main()
