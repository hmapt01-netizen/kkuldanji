"""Fault injection tests: temporary copies only; no posts written or deployments."""
from pathlib import Path
import contextlib
import io
import runpy
import shutil
import tempfile
import unittest
from unittest.mock import patch
import site_pagination_guard as guard
import audit_site
import add_post

ROOT=Path(__file__).resolve().parents[1]
class PaginationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.web=Path(self.tmp.name)
        for name in ['templates/index_template.html','index.html','css/style.css']:
            p=self.web/name;p.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(ROOT/'kkuldanji_web'/name,p)
    def mutate(self,name,old,new):
        p=self.web/name;s=p.read_text(encoding='utf-8-sig')
        self.assertIn(old,s);p.write_text(s.replace(old,new),encoding='utf-8')
    def check_blocked(self):
        with self.assertRaises(guard.PaginationError):guard.validate(self.web)
    def test_current_behavior_passes(self):
        guard.validate(self.web)
    def test_template_show_all_is_blocked(self):
        self.mutate('templates/index_template.html','pcShown = 6;','pcShown = 999;');self.check_blocked()
    def test_generated_page_regression_is_blocked(self):
        self.mutate('index.html','pcShown = 6;','pcShown = 999;');self.check_blocked()
    def test_wrong_load_more_size_is_blocked(self):
        self.mutate('templates/index_template.html','pcShown += 6;','pcShown += 12;');self.check_blocked()
    def test_tab_reset_removal_is_blocked(self):
        self.mutate('templates/index_template.html','pcShown = 6; // 새 카테고리는 첫 페이지부터 표시','// missing desktop reset');self.check_blocked()
    def test_css_button_override_is_blocked(self):
        self.mutate('css/style.css','.btn-load-more {\n    display: inline-flex;','.btn-load-more {\n    display: inline-flex !important;');self.check_blocked()
    def test_grid_columns_change_is_blocked(self):
        self.mutate('templates/index_template.html','grid-template-columns:repeat(3, 1fr)','grid-template-columns:repeat(4, 1fr)');self.check_blocked()
    def test_missing_template_and_runtime_fail_closed(self):
        with patch.object(guard,'node_executable',side_effect=guard.PaginationError('Node missing')):self.check_blocked()
        (self.web/'templates/index_template.html').unlink();self.check_blocked()
    def test_registration_stops_before_db_or_image_mutation(self):
        with patch('step_guard.check_step'),patch.object(guard,'validate',side_effect=guard.PaginationError('broken pagination')),patch('builtins.open') as opened,patch('shutil.copy2') as copied:
            with self.assertRaises(AssertionError):add_post.add_post({'title':'gate test'})
            opened.assert_not_called();copied.assert_not_called()
    def test_build_stops_before_reading_or_writing_posts(self):
        with patch.object(guard,'validate',side_effect=guard.PaginationError('broken pagination')),patch('builtins.open') as opened:
            with self.assertRaises(SystemExit) as stopped:runpy.run_path(str(ROOT/'tools/build_site.py'),run_name='__main__')
            self.assertEqual(stopped.exception.code,1);opened.assert_not_called()
    def test_audit_failure_prevents_live_requests(self):
        with patch.object(audit_site,'audit_local',return_value=([],audit_site.Counter())),patch.object(guard,'validate',side_effect=guard.PaginationError('broken pagination')),patch.object(audit_site,'audit_live') as live:
            self.assertEqual(audit_site.main(['--live']),1);live.assert_not_called()

if __name__=='__main__':unittest.main()
