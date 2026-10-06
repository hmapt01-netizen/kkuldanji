"""Offline behavioural tests; fixtures below are synthetic, never live evidence."""
import contextlib
import copy
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import quote

import topic_opportunity as t
import audit_serp_live as legacy
import serp_collection as collector
import validate_titles as titles


def judged():
    c = t.candidate('c1', 'fixture full question', [], 'hypothesis')
    c.update(reader_question='Fixture reader intent', duplication_note='Title-only overlap review; body unread',
             site_fit='Fixture editorial fit', answer_value='Hypothesis to validate during research')
    for ch in t.CHANNELS:
        c['channels'][ch].update(reason='Exploration worth comparing; no portal screen observed',
                                 uncertainty='Demand volume and body coverage unknown')
    return dict(version=1, stage='discovery', sources=[], candidates=[c], recommendations=['c1'],
                comparison_reason='Exploratory preference, withdraw if already answered', search_limits='Synthetic fixture only')


class TopicAgent(unittest.TestCase):
    def test_hypothesis_can_be_recommended_as_exploration_without_fake_metrics(self):
        report = t.render(judged(), {'posts': []})
        self.assertIn('탐색 후보', report)
        self.assertIn('AI 가설', report)
        self.assertNotIn('💎', report)

    def test_portal_comparison_requires_actual_matching_screen(self):
        r = judged()
        r['candidates'][0]['channels']['google']['verdict'] = 'compare'
        with self.assertRaises(ValueError):
            t.validate(r)
        query = r['candidates'][0]['query']
        r['sources'] = [dict(id='s1', kind='serp_screen', channel='google', query=query,
                            observed_at=t.now(), url='https://www.google.com/search?q='+quote(query),
                            excerpt='Fixture title/link observations')]
        r['candidates'][0]['channels']['google']['source_ids'] = ['s1']
        t.validate(r)
        r['sources'][0]['observed_at'] = '2020-01-01T00:00:00+09:00'
        with self.assertRaises(ValueError):
            t.validate(r)
        r['sources'][0]['observed_at'] = t.now()
        r['sources'][0]['query'] = 'different question'
        with self.assertRaises(ValueError):
            t.validate(r)

    def test_google_evidence_cannot_be_relabelled_as_naver(self):
        r = judged()
        r['sources'] = [dict(id='s1', kind='autocomplete', channel='google', query='fixture',
                            observed_at=t.now(), url='https://www.google.com/', excerpt='fixture')]
        r['candidates'][0]['channels']['naver']['source_ids'] = ['s1']
        with self.assertRaises(ValueError):
            t.validate(r)

    def test_no_fake_gsc_success_or_values(self):
        r = judged()
        source = dict(id='s1', kind='gsc', channel='google', query='q', page='https://honeyjar.co.kr/p',
                      observed_at=t.now(), url='https://search.google.com/search-console', excerpt='fixture',
                      metrics={'keys': ['q','https://honeyjar.co.kr/p'], 'impressions': 1}, period={'startDate':'2026-09-01'})
        r['sources'] = [source]
        with self.assertRaises(ValueError):
            t.validate(r, {'gsc': {'status': 'unavailable'}})
        ctx = {'gsc': {'status': 'ok', 'rows': [copy.deepcopy(source['metrics'])], 'request': source['period']}}
        t.validate(r, ctx)
        source['metrics']['impressions'] = 999
        with self.assertRaises(ValueError):
            t.validate(r, ctx)

    def test_new_post_and_existing_update_are_separate(self):
        r = judged()
        r['candidates'][0]['action'] = 'update'
        with self.assertRaises(ValueError):
            t.validate(r)
        r['candidates'][0]['existing_slugs'] = ['existing']
        t.validate(r, {'posts': [{'slug': 'existing'}]})

    def test_duplicate_queries_not_multiple_recommendations(self):
        r = judged()
        c = copy.deepcopy(r['candidates'][0]); c['id'] = 'c2'
        r['candidates'].append(c); r['recommendations'].append('c2')
        with self.assertRaises(ValueError):
            t.validate(r)

    def test_prepare_never_fills_recommendations_or_overwrites_work(self):
        with tempfile.TemporaryDirectory() as folder:
            r = t.prepare(folder, ['fixture'], use_gsc=False, collect=False)
            self.assertEqual(r['recommendations'], [])
            with self.assertRaises(ValueError):
                t.report(folder)
            before = (Path(folder) / 'topic_review.json').read_bytes()
            with self.assertRaises(ValueError):
                t.prepare(folder, ['changed'], use_gsc=False, collect=False)
            self.assertEqual(before, (Path(folder) / 'topic_review.json').read_bytes())

    def test_report_rejects_changed_context_and_unbacked_sources(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            initial = t.prepare(work, [], use_gsc=False, collect=False)
            r = judged(); r['context_sha256'] = initial['context_sha256']
            (work / 'topic_review.json').write_text(json.dumps(r), encoding='utf-8')
            self.assertIn('잠정 추천', t.report(work))
            r['sources'] = [dict(id='extra', kind='web_search', channel='web', query='fixture',
                                observed_at=t.now(), url='https://example.org', excerpt='fixture')]
            (work / 'topic_review.json').write_text(json.dumps(r), encoding='utf-8')
            with self.assertRaises(ValueError):
                t.report(work)
            (work / 'evidence.txt').write_text('fixture', encoding='utf-8')
            r['sources'][0].update(evidence_file='evidence.txt', evidence_sha256=hashlib.sha256(b'fixture').hexdigest())
            (work / 'topic_review.json').write_text(json.dumps(r), encoding='utf-8')
            t.report(work)
            (work / 'topic_context.json').write_text('{}', encoding='utf-8')
            with self.assertRaises(ValueError):
                t.report(work)

    def test_legacy_entrypoint_uses_shared_collector(self):
        self.assertIs(legacy.audit_titles, collector.audit_titles)
        query = 'one two three four five six seven'
        self.assertEqual(legacy.extract_clean_query_and_seed(query), (query, query))
        self.assertIn('추가 조사', legacy.analyze_google_competition(query, [], query)[0])

    def test_no_search_means_no_positive_badge_no_audit_writes(self):
        sample = ['“fixture question” text long enough for check '+str(n) for n in range(10)]
        with patch.object(titles, 'audit_titles') as collect, patch('builtins.open') as write, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertTrue(titles.validate_google_titles(sample, run_serp=False))
            self.assertTrue(titles.validate_naver_titles(sample, run_serp=False))
        collect.assert_not_called(); write.assert_not_called()
        self.assertNotIn('알짜 틈새', out.getvalue())

    def test_title_search_without_explicit_queries_never_contacts_network(self):
        with patch.object(titles, 'audit_titles') as collect:
            with self.assertRaises(ValueError):
                titles.collect_title_evidence(['headline'], 'google', None)
        collect.assert_not_called()

    def test_guard_rejects_fake_badge_failed_or_empty_collection(self):
        from test_blue_ocean import reviewed
        row = reviewed()
        self.assertTrue(collector.usable_collection(row, 'naver'))
        row['top_docs'] = []
        self.assertFalse(collector.usable_collection(row, 'naver'))
        row.update(badge='💎', collection_status='error')
        self.assertFalse(collector.usable_collection(row, 'naver'))

    def test_feedback_appends_original_decision_hash_without_changing_review(self):
        with tempfile.TemporaryDirectory() as folder:
            work = Path(folder)
            t.prepare(work, ['fixture'], use_gsc=False, collect=False)
            before = (work / 'topic_review.json').read_bytes()
            with patch.object(t, 'gsc_snapshot', return_value={'status': 'unavailable', 'rows': []}):
                t.feedback(work, 'c1', 'https://honeyjar.co.kr/posts/fixture.html', 'Fixture only')
                t.feedback(work, 'c1', 'https://honeyjar.co.kr/posts/fixture.html', 'Second fixture only')
            self.assertEqual(before, (work / 'topic_review.json').read_bytes())
            rows = [json.loads(s) for s in (work / 'topic_outcomes.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]['gsc']['status'], 'unavailable')
            self.assertEqual(rows[0]['review_sha256'], hashlib.sha256(before).hexdigest())

    def test_title_stage_does_not_require_research_and_still_requires_selection(self):
        import step_guard as g
        with tempfile.TemporaryDirectory() as folder, patch.object(g, 'verify_research_facts') as research, contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(g.check_step(1, folder))
            research.assert_not_called()
            with self.assertRaises(SystemExit):
                g.check_step(3, folder)
            research.assert_not_called()

    def test_summary_comparison_never_requires_or_claims_body_review(self):
        import sys
        sys.path.insert(0, str(t.ROOT / 'codex_tools'))
        import title_adapter as adapter
        from test_blue_ocean import reviewed
        row = reviewed(); row['review'] = {}
        for doc in row['top_docs']:
            doc.update(answer_coverage='unreviewed', review_note='', reviewed_at='')
        row['title'] = row['clean_query']
        row['title_review'] = dict(scope='title_summary', competition='medium', reason='Title-only fixture comparison', reviewed_at=t.now())
        row['related_keyword'] = dict(text=row['clean_query'], source_url='https://ac.search.naver.com', observed_at=t.now())
        result, score = adapter.assessed(row)
        self.assertTrue(result['comparison_ready'])
        self.assertFalse(result['evidence_complete'])
        self.assertIn('본문 답변 누락 미확인', result['review_scope'])
        self.assertIsNone(score)


if __name__ == '__main__':
    unittest.main()
