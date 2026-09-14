"""Offline regression tests. No Git commands, cloud requests, or live comments."""
import json
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

import audit_site


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'web'
        self.root.mkdir()
        for name in audit_site.REQUIRED:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('asset', encoding='utf-8')
            if path.suffix == '.html':
                path.write_text('<link rel="icon" href="favicon.ico"><main id="ok"></main>'
                                + '<!--' + 'x' * 3000 + '-->', encoding='utf-8')
        with (self.root / 'contact.html').open('a', encoding='utf-8') as f:
            f.write('<form><input id="user-name"><input id="user-email">'
                    '<textarea id="user-message"></textarea></form>')
        (self.root / 'posts').mkdir()
        (self.root / 'posts/한글.html').write_text(
            '<link rel="icon" href="../favicon.ico"><main id="section"></main>', encoding='utf-8')
        registry = [{'slug': '한글.html', 'thumb': 'favicon.ico'}]
        (self.root / 'js/features.js').write_text(
            'window.HONEYJAR_POSTS_REGISTRY = window.HONEYJAR_POSTS_REGISTRY || '
            + json.dumps(registry) + ';', encoding='utf-8')
        (self.root.parent / 'data').mkdir()
        (self.root.parent / 'data/posts_db.json').write_text(json.dumps(registry), encoding='utf-8')

    def append(self, value):
        with (self.root / 'index.html').open('a', encoding='utf-8') as f:
            f.write(value)

    def errors(self):
        with patch('urllib.request.urlopen', side_effect=AssertionError('Network forbidden')):
            return audit_site.audit_local(self.root)[0]

    def test_valid_local_site_never_calls_network(self):
        self.assertEqual(self.errors(), [])

    def test_directory_category_link_fails_but_explicit_index_passes(self):
        self.append('<a href="./?cat=식단">bad</a><a href="index.html?cat=식단">good</a>')
        errors = self.errors()
        self.assertEqual(len(errors), 1)
        self.assertIn('폴더 링크', errors[0][2])

    def test_encoded_root_path_query_fragment_and_top(self):
        self.append('<a href="/posts/%ED%95%9C%EA%B8%80.html?v=2#section">ok</a>'
                    '<a href="#top">top</a><a href="#ok">ok</a>')
        self.assertEqual(self.errors(), [])

    def test_missing_file_fragment_asset_and_path_escape_fail(self):
        self.append('<a href="missing.html">bad</a><a href="#missing">bad</a>'
                    '<script src="missing.js?v=2"></script><a href="../outside">bad</a>')
        errors = self.errors()
        self.assertEqual(len(errors), 4)
        self.assertEqual(sum(e[0] == 'asset' for e in errors), 1)

    def test_parser_ignores_markup_in_script_and_comments_but_catches_nesting(self):
        self.append('<script>const html="<div>";</script><!-- <main> -->')
        self.assertEqual(self.errors(), [])
        self.append('<div><section></div></section>')
        self.assertTrue(any(e[0] == 'html' for e in self.errors()))

    def test_single_bom_valid_duplicate_bom_and_invalid_utf8_fail(self):
        path = self.root / 'index.html'
        raw = path.read_bytes()
        path.write_bytes(b'\xef\xbb\xbf' + raw)
        self.assertEqual(self.errors(), [])
        path.write_bytes(b'\xef\xbb\xbf\xef\xbb\xbf' + raw)
        self.assertTrue(any(e[0] == 'encoding' for e in self.errors()))
        path.write_bytes(raw + b'\xff')
        self.assertTrue(any(e[0] == 'encoding' for e in self.errors()))

    def test_deleted_required_file_and_registry_drift_fail(self):
        (self.root / 'robots.txt').unlink()
        (self.root.parent / 'data/posts_db.json').write_text('[]', encoding='utf-8')
        errors = self.errors()
        self.assertTrue(any(e[1] == 'robots.txt' for e in errors))
        self.assertTrue(any('불일치' in e[2] for e in errors))

    def test_local_failure_skips_live_and_returns_nonzero(self):
        with patch.object(audit_site, 'audit_local', return_value=([('link','index','bad')], audit_site.Counter())), \
             patch.object(audit_site, 'audit_live') as live:
            self.assertEqual(audit_site.main(['--live']), 1)
            live.assert_not_called()


class DeploymentGateTests(unittest.TestCase):
    def run_deploy(self, returncode, check_only=False):
        source = Path(__file__).with_name('deploy_site.py')
        fake_publish = types.ModuleType('publish_article')
        fake_publish.validate_all_cards = lambda *args: True
        with patch.object(sys, 'argv', [str(source)] + (['--check-only'] if check_only else [])), \
             patch.dict(sys.modules, {'publish_article': fake_publish}), \
             patch('subprocess.run', return_value=subprocess.CompletedProcess([], returncode)) as run:
            with self.assertRaises(SystemExit) as stopped:
                runpy.run_path(str(source), run_name='__main__')
            self.assertEqual(stopped.exception.code, returncode)
            self.assertEqual(run.call_count, 1, 'Must stop before any Git/indexing command')
            self.assertIn('--local', run.call_args.args[0])

    def test_failed_audit_stops_before_git(self):
        self.run_deploy(1)

    def test_check_only_stops_before_git_even_when_audit_passes(self):
        self.run_deploy(0, check_only=True)


if __name__ == '__main__':
    unittest.main()
