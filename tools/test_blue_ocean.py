"""Regression checks for false blue-ocean positives; offline fixtures only."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

import blue_ocean as b
import serp_collection as c
import suggest_topics as s
import validate_titles as v
from audit_serp_live import extract_clean_query_and_seed


def stamp():
    return datetime.now(timezone.utc).isoformat()


def reviewed():
    query = 'fixture exact question'
    return {'idx': 1, 'title': query, 'clean_query': query,
            'collection_status': 'ok', 'collection_method': 'browser', 'collected_at': stamp(),
            'search_url': 'https://search.naver.com/search.naver?query=' + quote(query),
            'top_docs': [{'rank': i, 'url': f'https://example.org/article/{i}', 'title': f'Fixture {i}',
                          'answer_coverage': 'partial', 'review_note': 'Fixture page covers context but omits the asked condition.',
                          'reviewed_at': stamp()} for i in range(1, 11)],
            'review': {'query': query, 'reader_question': query, 'reviewed_at': stamp(),
                       'demand': [{'kind': 'search_impressions', 'query': query,
                                   'source_url': 'https://search.google.com/search-console',
                                   'observed_at': stamp(), 'period': 'fixture period', 'value': 25,
                                   'interpretation': 'Fixture-only exact-query impressions.'}],
                       'competition': 'gap', 'competition_reason': 'Fixture reviewed pages omit the requested condition.',
                       'gap': 'Unanswered condition', 'answer_plan': 'Compare conditions using source passages.',
                       'sources': [{'url': 'https://source-one.org/report', 'finding': 'Fixture passage one', 'checked_at': stamp()},
                                   {'url': 'https://source-two.org/report', 'finding': 'Fixture passage two', 'checked_at': stamp()}],
                       'duplication_review': 'Fixture existing body compared; different intent.',
                       'decision_reason': 'Fixture demand, gap and sources present.'}}


class Parsing(unittest.TestCase):
    def test_ads_shopping_tracking_and_duplicate_urls(self):
        html = '''<a class="title_link" href="https://ader.naver.com/click?a=1">Long advertisement</a>
        <div class="sponsored"><a href="https://advertiser.org/"><h3>Sponsored title</h3></a></div>
        <a class="title_link" href="https://shopping.naver.com/product">Shopping result</a>
        <a class="title_link" href="https://example.org/post?id=3&amp;utm_source=naver#x">Real title</a>
        <a class="title_link" href="https://example.org/post?id=3">Duplicate title</a>
        <a href="https://example.org/nav">Very long navigation that is not a result title</a>'''
        docs, excluded = b.parse_serp(html, 'naver')
        self.assertEqual([d['url'] for d in docs], ['https://example.org/post?id=3'])
        self.assertEqual(len(excluded), 3)

    def test_google_heading_and_redirect(self):
        docs, _ = b.parse_serp('<a href="/url?q=https%3A%2F%2Fexample.org%2Freport"><h3>A real result</h3></a>', 'google')
        self.assertEqual(docs[0]['url'], 'https://example.org/report')

    def test_current_naver_ugc_titles_not_source_or_snippet(self):
        html = '''<a data-heatmap-target="articleSourceJSX_title" href="https://blog.naver.com/name">Source profile name</a>
        <a data-heatmap-target=".imgtitlelink" class="random_hash" href="https://blog.naver.com/name/123">Actual title 새 창 열림</a>
        <a data-heatmap-target=".imgtitlelink" class="fds-ugc-ellipsis2" href="https://blog.naver.com/name/124">Snippet text</a>'''
        docs, _ = b.parse_serp(html, 'naver')
        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]['title'], 'Actual title')

    def test_web_profile_is_not_title(self):
        html = '''<a data-heatmap-target=".link" href="https://example.org/post"><div data-sds-comp="Profile">Example profile example.org</div></a>
        <a data-heatmap-target=".link" href="https://example.org/post"><span class="sds-comps-text-type-headline1">Actual article title</span></a>'''
        docs, _ = b.parse_serp(html, 'naver')
        self.assertEqual(docs[0]['title'], 'Actual article title')

    def test_full_urls_and_ids_not_truncated(self):
        url = 'https://example.org/' + 'a' * 150 + '?id=1'
        docs, _ = b.parse_serp(f'<a class="title_link" href="{url}">Long URL title</a>', 'naver')
        self.assertEqual(docs[0]['url'], url)
        self.assertNotEqual(b.canonical_url(url), b.canonical_url(url.replace('id=1', 'id=2')))

    def test_empty_results_do_not_imply_gap(self):
        with patch.object(c, 'read_url', return_value='<html>unknown layout</html>'):
            result = c.fetch_serp('naver', 'query')
        self.assertEqual(result['collection_status'], 'error')

    def test_captcha_not_results(self):
        with patch.object(c, 'read_url', return_value='<html>unusual traffic</html>'):
            self.assertEqual(c.fetch_serp('google', 'query')['collection_status'], 'error')

    def test_autocomplete_failure_distinct_from_empty(self):
        with patch.object(c, 'read_url', side_effect=OSError('offline')):
            self.assertEqual(c.autocomplete('google', 'query')['status'], 'error')
        with patch.object(c, 'read_url', return_value='["query", []]'):
            self.assertEqual(c.autocomplete('google', 'query')['status'], 'ok')


class Evidence(unittest.TestCase):
    def test_complete_review_priority_and_hold(self):
        r = reviewed()
        self.assertEqual(b.evaluate(r)['status'], 'priority')
        r['review']['competition'] = 'high'
        self.assertEqual(b.evaluate(r)['status'], 'hold')

    def test_missing_evidence_cannot_pass(self):
        for field in ('demand', 'sources', 'answer_plan', 'duplication_review', 'gap'):
            with self.subTest(field=field):
                r = reviewed()
                r['review'].pop(field)
                self.assertFalse(b.evaluate(r)['evidence_complete'])

    def test_autocomplete_never_proves_demand(self):
        r = reviewed()
        r['autocomplete_count'] = 100
        r['review']['demand'][0]['kind'] = 'autocomplete'
        self.assertEqual(b.evaluate(r)['status'], 'additional_research')

    def test_nonpositive_or_invalid_metrics(self):
        for value in (0, -2, True, '100', float('nan'), float('inf')):
            r = reviewed()
            r['review']['demand'][0]['value'] = value
            self.assertFalse(b.evaluate(r)['evidence_complete'])

    def test_seed_metric_not_exact_query_evidence(self):
        r = reviewed()
        r['review']['demand'][0]['query'] = 'broad seed'
        self.assertFalse(b.evaluate(r)['evidence_complete'])

    def test_repeated_questions_require_distinct_sources(self):
        r = reviewed()
        e = r['review']['demand'][0]
        e['kind'] = 'repeated_questions'
        self.assertFalse(b.evaluate(r)['evidence_complete'])
        e['question_urls'] = ['https://example.org/q/1', 'https://example.org/q/2']
        self.assertTrue(b.evaluate(r)['evidence_complete'])

    def test_unreviewed_doc_blocks_positive_badge(self):
        r = reviewed()
        r['top_docs'][3]['answer_coverage'] = 'unreviewed'
        r['badge'] = '💎'; r['status'] = 'priority'
        self.assertFalse(b.evaluate(r)['evidence_complete'])

    def test_fewer_than_ten_needs_scope_note(self):
        r = reviewed()
        r['top_docs'] = r['top_docs'][:5]
        self.assertFalse(b.evaluate(r)['evidence_complete'])
        r['coverage_note'] = 'Fixture screen verified: only five organic results.'
        self.assertTrue(b.evaluate(r)['evidence_complete'])
        r['top_docs'] = []
        self.assertFalse(b.evaluate(r)['evidence_complete'])

    def test_stale_and_future_records(self):
        for delta in (-25, 2):
            r = reviewed()
            r['collected_at'] = (datetime.now(timezone.utc) + timedelta(hours=delta)).isoformat()
            self.assertFalse(b.evaluate(r)['evidence_complete'])

    def test_source_and_duplicate_validation(self):
        for url in ('https://ader.naver.com/click', 'not a URL', 'https://example.org/article/1'):
            r = reviewed()
            r['top_docs'][1]['url'] = url
            self.assertFalse(b.evaluate(r)['evidence_complete'])

    def test_guard_rejects_old_schema_wrong_channel_and_query(self):
        data = {'schema_version': 2, 'timestamp': stamp(), 'channel': 'naver', 'records': [reviewed()]}
        self.assertEqual(b.audit_errors(data), [])
        for key, value in (('schema_version', 1), ('channel', 'google')):
            bad = dict(data, **{key: value})
            self.assertTrue(b.audit_errors(bad))
        data['records'][0]['clean_query'] = 'different question'
        self.assertTrue(b.audit_errors(data))

    def test_import_failure_does_not_replace_good_audit(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(c, 'DATA_DIR', Path(tmp)):
            source = Path(tmp) / 'review.json'
            data = {'schema_version': 2, 'timestamp': stamp(), 'channel': 'naver', 'records': [reviewed()]}
            source.write_text(json.dumps(data), encoding='utf-8')
            with contextlib.redirect_stdout(io.StringIO()):
                c.import_review(source)
            target = Path(tmp) / 'last_serp_audit.json'
            before = target.read_bytes()
            data['records'][0]['review']['demand'] = []
            source.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaises(ValueError):
                c.import_review(source)
            self.assertEqual(target.read_bytes(), before)


class Integration(unittest.TestCase):
    def test_query_preserves_long_tail_condition(self):
        query = '섭취 순서 식사 전에 먹으면 어떻게 되나'
        self.assertEqual(extract_clean_query_and_seed(query)[0], query)

    def test_candidate_report_does_not_claim_unperformed_checks(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(s, 'root_dir', tmp), \
             patch.object(s, 'fetch_portal_suggestions', return_value=['두유 영양 비교']), \
             patch.object(s, 'fetch_live_news_trends', return_value=[]), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            (Path(tmp) / 'data').mkdir()
            s.run_topic_suggestion('두유')
            saved = json.loads((Path(tmp) / 'data/last_topic_audit.json').read_text(encoding='utf-8'))
        self.assertIsNone(saved['top_pick'])
        self.assertNotIn('PASS', output.getvalue())
        self.assertNotIn('검색수요 0건', output.getvalue())

    def test_discovery_never_recommends_unreviewed_candidate(self):
        for terms in ([], ['query one', 'query two']):
            self.assertTrue(all(x['status'] == 'additional_research' for x in s.build_dynamic_candidates_from_queries('seed', terms)))

    def test_google_actually_fetches_serp_and_preserves_legacy_keys(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(c, 'DATA_DIR', Path(tmp)), \
             patch.object(c, 'autocomplete', return_value={'status':'ok', 'items':[], 'error':None}), \
             patch.object(c, 'fetch_serp', return_value={'top_docs':[], 'collection_status':'error'}) as fetch, \
             contextlib.redirect_stdout(io.StringIO()):
            records = c.audit_google_serp(['영양제 복용 시간 질문'])
            fetch.assert_called_once()
            self.assertEqual(fetch.call_args.args[0], 'google')
            self.assertTrue({'idx','title','clean_query','seed','badge','reason','top_docs'} <= records[0].keys())
            self.assertEqual(records[0]['status'], 'additional_research')

    def test_title_renderer_does_not_trust_fake_badge(self):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            pick = v.render_evidence_table([{'idx':1,'title':'fake','badge':'💎','status':'priority','reason':'fake'}])
        self.assertIsNone(pick)
        self.assertIn('추천 보류', output.getvalue())
        self.assertNotIn('💎', output.getvalue())


if __name__ == '__main__':
    unittest.main()
