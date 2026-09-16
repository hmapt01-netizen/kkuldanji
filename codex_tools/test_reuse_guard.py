"""Offline checks for research handoff and execution boundaries."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import reuse_guard as r
import workflow_guard as g


def fixture(work, stage):
    path = work / 'reuse_fixture.txt'
    path.write_text('Verified fixture source and conditions.', encoding='utf-8')
    ref = {'path': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
           'excerpt': 'Verified fixture source and conditions.'}
    data = {'version': 1, 'stage': stage, 'selected_titles': r.selections(work, stage),
            'intent': 'Fixture answer scope', 'reviewed_existing': [ref],
            'questions': [{'question': 'Fixture reader question', 'mode': 'reuse',
                           'evidence': [ref], 'answer': 'Fixture supported answer',
                           'limits': 'Fixture conditions', 'body_location': 'Fixture body section'}]}
    path = work / r.filename(stage)
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data), encoding='utf-8')
    return data


class Reuse(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name)
        self.data = fixture(self.work, 'draft')

    def save(self):
        (self.work / r.filename('draft')).write_text(json.dumps(self.data), encoding='utf-8')

    def test_existing_sources_can_finish_without_additional_search(self):
        self.assertIn('reuse_fixture.txt', r.validate(self.work, 'draft', complete=True))

    def test_additional_research_needs_reason_and_saved_result(self):
        q = self.data['questions'][0]
        q.update(mode='additional', evidence=[])
        self.save()
        with self.assertRaises(ValueError):
            r.validate(self.work, 'draft')
        q.update(reason='The selected scope is not covered.', reason_type='missing')
        self.save()
        r.validate(self.work, 'draft')
        with self.assertRaisesRegex(ValueError, '저장 근거'):
            r.validate(self.work, 'draft', complete=True)

    def test_changed_evidence_and_wrong_excerpt_rejected(self):
        (self.work / 'reuse_fixture.txt').write_text('Changed by another editor', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, '재검토'):
            r.validate(self.work, 'draft')
        self.data = fixture(self.work, 'draft')
        self.data['questions'][0]['evidence'][0]['excerpt'] = 'Not present'
        self.save()
        with self.assertRaisesRegex(ValueError, '발췌'):
            r.validate(self.work, 'draft')

    def test_title_change_requires_handoff_update(self):
        (self.work / g.STATE).write_text(json.dumps({'receipts': [
            {'stage': 'naver_selection', 'selected_title': 'Chosen title'}]}), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, '선택 제목'):
            r.validate(self.work, 'draft')

    def test_draft_requires_body_mapping_and_cannot_exclude_every_question(self):
        self.data['questions'][0]['body_location'] = ''
        self.save()
        with self.assertRaisesRegex(ValueError, '본문'):
            r.validate(self.work, 'draft', complete=True)
        self.data['questions'][0].update(mode='exclude', reason='Outside scope')
        self.save()
        with self.assertRaisesRegex(ValueError, '모든 질문'):
            r.validate(self.work, 'draft', complete=True)

    def test_entry_and_record_cannot_skip_manifest(self):
        (self.work / 'post_data.json').write_text(json.dumps({'title': None, 'bodyHtml': '<p>Fixture body</p>'}), encoding='utf-8')
        (self.work / r.filename('draft')).unlink()
        with patch.object(g, 'next_step', return_value=('draft', '')), \
                patch('freshness_guard.validate', return_value=[]):
            with self.assertRaisesRegex(ValueError, '자료 인계 누락'):
                g.require_step(self.work, 'draft')
            with self.assertRaisesRegex(ValueError, '자료 인계 누락'):
                g.record(self.work, 'draft', [], 'Attempt')
        self.assertFalse((self.work / g.STATE).exists())

    def test_collector_stops_before_network_without_manifest(self):
        import title_adapter
        with patch.object(g, 'next_step', return_value=('naver_titles', '')), \
                patch('freshness_guard.validate', return_value=[]), \
                patch.object(title_adapter.collector, 'audit_titles') as network:
            with self.assertRaisesRegex(ValueError, '자료 인계 누락'):
                title_adapter.collect(self.work, {}, 'naver')
            network.assert_not_called()

    def test_init_is_unfinished_and_never_overwrites(self):
        r.init(self.work, 'research', ['Unanswered question'])
        with self.assertRaises(ValueError):
            r.validate(self.work, 'research')
        with self.assertRaises(FileExistsError):
            r.init(self.work, 'research', ['Other question'])

    def test_evidence_outside_work_rejected(self):
        self.data['reviewed_existing'][0]['path'] = '../outside.txt'
        self.save()
        with self.assertRaises(ValueError):
            r.validate(self.work, 'draft')


if __name__ == '__main__':
    unittest.main()
