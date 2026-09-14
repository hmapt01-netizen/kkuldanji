"""Exercise the actual feed build section in a temp folder; never deploy."""
import contextlib
import datetime
import io
import os
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import audit_site


class FeedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.posts = [dict(slug='first.html', title='첫 글 & 제목',
                           desc='원래 설명', category='식단 & 영양', date='2026.09.14')]
        source = Path(__file__).with_name('build_site.py').read_text(encoding='utf-8-sig')
        self.build_source = source[source.index('def parse_korean_date_to_rfc822'):]
        self.build_source = self.build_source.split('\nimport subprocess\n')[0]
        self.build()

    def build(self):
        env = dict(os=os, re=re, datetime=datetime, posts=self.posts,
                   web_root=str(self.root), force_full_build=False)
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(self.build_source, 'build_site.py:feed-section', 'exec'), env)

    def test_new_post_and_revision_reach_both_addresses(self):
        self.posts[0]['desc'] = '수정된 설명'
        self.posts.insert(0, dict(slug='new.html', title='새 글', desc='새 설명',
                                 category='라이프 웰니스', date='2026.09.15'))
        self.build()
        self.assertEqual(audit_site.audit_feeds(self.root, self.posts), [])
        for name in ('feed.xml', 'rss.xml'):
            items = ET.parse(self.root / name).findall('./channel/item')
            self.assertEqual(len(items), 2)
            self.assertEqual(items[1].findtext('description'), '수정된 설명')

    def test_incremental_build_repairs_legacy_feed_without_touching_current(self):
        feed = self.root / 'feed.xml'
        before = feed.stat().st_mtime_ns
        (self.root / 'rss.xml').write_text('<rss/>', encoding='utf-8')
        self.build()
        self.assertEqual(feed.stat().st_mtime_ns, before)
        self.assertEqual(audit_site.audit_feeds(self.root, self.posts), [])
        (self.root / 'rss.xml').unlink()
        self.build()
        self.assertEqual(audit_site.audit_feeds(self.root, self.posts), [])

    def test_no_change_build_preserves_both_files(self):
        before = {p.name: p.stat().st_mtime_ns for p in self.root.glob('*.xml')}
        self.build()
        self.assertEqual(before, {p.name: p.stat().st_mtime_ns for p in self.root.glob('*.xml')})

    def test_audit_blocks_missing_malformed_and_stale_feed(self):
        path = self.root / 'rss.xml'
        for bad in ('<rss>', path.read_text(encoding='utf-8').replace('원래 설명', '오래된 설명')):
            with self.subTest(bad=bad[:20]):
                path.write_text(bad, encoding='utf-8')
                self.assertTrue(audit_site.audit_feeds(self.root, self.posts))
        path.unlink()
        self.assertTrue(audit_site.audit_feeds(self.root, self.posts))

    def test_audit_rejects_unbuilt_new_post(self):
        self.posts.append(dict(slug='missing.html', title='누락', date='2026.09.15'))
        self.assertEqual(len(audit_site.audit_feeds(self.root, self.posts)), 2)

    def test_local_feed_failure_prevents_network_audit(self):
        with patch.object(audit_site, 'audit_local', return_value=(
                [('rss', 'rss.xml', 'stale')], audit_site.Counter())), \
                patch('site_pagination_guard.validate'), \
                patch.object(audit_site, 'audit_live') as live:
            self.assertEqual(audit_site.main(['--live']), 1)
            live.assert_not_called()


if __name__ == '__main__':
    unittest.main()
