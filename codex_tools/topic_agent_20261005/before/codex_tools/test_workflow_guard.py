"""Offline regressions for Codex-specific skip, early-stop and title rules."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.parse import quote
import title_adapter as adapter
import workflow_guard as g
import report_guard as report
from test_blue_ocean import reviewed, stamp


class Workflow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        from test_freshness_guard import fixture
        fixture(self.work)
        record = reviewed()
        self.put('serp.json', {'schema_version': 2, 'timestamp': stamp(), 'channel': 'naver', 'records': [record]})
        self.put('codex_target.json', {'site_fit': 'core', 'site_fit_reason': 'Fixture fit', 'channels': {
            'naver': {'query': 'fixture exact question', 'intent_terms': ['fixture', 'question'], 'evidence_file': 'serp.json'}}})
        (self.work / '리서치.md').write_text('Fixture research', encoding='utf-8')
        from test_reuse_guard import fixture as reuse_fixture
        reuse_fixture(self.work, 'research')
        reuse_fixture(self.work, 'naver_titles')
        self.research_files = ['리서치.md', 'codex_target.json', 'serp.json']
        self.title_files = ['naver_candidates.json', 'naver_serp_audit.json', 'naver_report.md', 'naver_related_keywords.json']
        self.titles = ['“fixture exact question” ' + str(i) + '가' * 18 for i in range(10)]
        self.put('naver_candidates.json', {'naver_candidates': self.titles,
            'search_queries': [f'fixture exact question {i}' for i in range(10)], 'intent_reviews': [
            {'title': t, 'query': 'fixture exact question', 'reason': 'Fixture intent match', 'reviewed_at': stamp()}
            for t in self.titles]})
        rows = []
        for i, title in enumerate(self.titles):
            row = copy.deepcopy(record)
            query = f'fixture exact question {i}'
            row.update(idx=i+1, title=title, clean_query=query, search_url='https://search.naver.com/search.naver?query='+quote(query))
            row['review']['query'] = query
            for demand in row['review']['demand']:
                demand['query'] = query
            rows.append(row)
        self.put('naver_serp_audit.json', {'schema_version': 2, 'timestamp': stamp(), 'channel': 'naver', 'records': rows})
        self.put('naver_related_keywords.json', {'channel':'naver','records':[{'status':'ok','items':[f'fixture exact question {i}' for i in range(10)], 'source_url':'https://ac.search.naver.com/nx/ac?q=fixture','observed_at':stamp()}]})
        (self.work / 'naver_report.md').write_text(report.expected_report(self.work, 'naver'), encoding='utf-8')

    def put(self, name, data):
        (self.work / name).write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def research(self):
        g.record(self.work, 'research', self.research_files, 'Fixture research reviewed')

    def proposed(self):
        self.research()
        g.record(self.work, 'naver_titles', self.title_files, 'Fixture titles actually presented')

    def command(self, *args):
        with patch('sys.argv', ['guard', '--work-dir', str(self.work), *args]), contextlib.redirect_stdout(io.StringIO()):
            return g.main()

    def test_cannot_finish_before_research_or_titles(self):
        self.assertEqual(self.command('finish'), 2)
        self.research()
        self.assertEqual(self.command('finish'), 2)

    def test_cannot_skip_naver_selection_in_two_track(self):
        self.proposed()
        self.assertEqual(self.command('check', '--stage', 'google_titles'), 2)

    def test_wait_only_after_valid_titles_presented(self):
        self.proposed()
        self.assertEqual(self.command('finish', '--reply-file', 'naver_report.md'), 0)
        self.assertEqual(g.next_step(self.work, g.state_of(self.work))[0], 'naver_selection')

    def test_no_fabricated_empty_approval(self):
        self.proposed()
        with self.assertRaises(ValueError):
            g.record(self.work, 'naver_selection', [], 'Fixture', selected_title=self.titles[0])

    def test_selected_title_must_belong_to_current_list(self):
        self.proposed()
        with self.assertRaises(ValueError):
            g.record(self.work, 'naver_selection', [], 'Fixture', 'User chose 1', 'not a candidate')

    def test_selection_continues_to_google_without_extra_permission(self):
        self.proposed()
        g.record(self.work, 'naver_selection', [], 'Fixture chosen', 'User chose 1', self.titles[0])
        self.assertEqual(g.next_step(self.work, g.state_of(self.work))[0], 'google_titles')
        self.assertEqual(self.command('finish'), 2)

    def test_title_length_boundaries_for_both_channels(self):
        for channel in ('naver', 'google'):
            for length, allowed in ((39, False), (40, True), (60, True), (61, False)):
                data = {channel + '_candidates': ['“' + str(i) + '가' * (length - 2) for i in range(10)]}
                if allowed:
                    self.assertEqual(len(g.titles_check(data, channel)), 10)
                else:
                    with self.assertRaises(ValueError):
                        g.titles_check(data, channel)

    def test_changed_evidence_returns_to_research(self):
        self.proposed()
        (self.work / '리서치.md').write_text('changed', encoding='utf-8')
        self.assertEqual(g.next_step(self.work, g.state_of(self.work))[0], 'research')
        self.assertEqual(self.command('finish'), 2)

    def test_adding_google_query_does_not_reset_naver_selection(self):
        self.proposed()
        target = g.read(self.work / 'codex_target.json')
        target['channels']['google'] = {'query': 'new google question'}
        self.put('codex_target.json', target)
        self.assertEqual(g.next_step(self.work, g.state_of(self.work))[0], 'naver_selection')

    def test_unreviewed_query_and_title_intent_drift_rejected(self):
        self.research()
        data = g.read(self.work / 'naver_candidates.json')
        data['search_queries'][0] = 'broad gift keyword'
        self.put('naver_candidates.json', data)
        with self.assertRaises(ValueError):
            g.record(self.work, 'naver_titles', self.title_files, 'Fixture')

    def test_title_evidence_mismatch_rejected_even_at_valid_length(self):
        self.research()
        data = g.read(self.work / 'naver_candidates.json')
        title = '“broad gift” ' + '가' * 30
        data['naver_candidates'][0] = title
        data['intent_reviews'][0]['title'] = title
        self.put('naver_candidates.json', data)
        with self.assertRaises(ValueError):
            g.record(self.work, 'naver_titles', self.title_files, 'Fixture')

    def test_repair_preserves_old_receipts_and_files(self):
        self.proposed()
        (self.work / '리서치.md').write_text('review corrected', encoding='utf-8')
        self.research()
        state = g.state_of(self.work)
        self.assertTrue(state['superseded'])
        self.assertTrue((self.work / 'naver_candidates.json').exists())
        self.assertEqual(g.next_step(self.work, state)[0], 'naver_titles')

    def test_path_outside_work_rejected(self):
        with self.assertRaises(ValueError):
            g.inside(self.work, '../not-our-file')

    def test_finish_requires_actual_reply_even_with_valid_receipts(self):
        self.proposed()
        self.assertEqual(self.command('finish'), 2)

    def test_old_title_only_reply_is_rejected(self):
        self.proposed()
        (self.work / 'old_reply.md').write_text('\n'.join(self.titles), encoding='utf-8')
        self.assertEqual(self.command('finish', '--reply-file', 'old_reply.md'), 2)

    def test_missing_report_cannot_record_titles(self):
        self.research()
        with self.assertRaises(ValueError):
            g.record(self.work, 'naver_titles', self.title_files[:-1], 'Fixture')

    def test_report_tampering_rejected_including_header_only_table(self):
        original = report.expected_report(self.work, 'naver')
        lines = original.splitlines(keepends=True)
        variants = {
            'all candidate rows removed': ''.join(line for line in lines if not any(line.startswith(f'| {i} |') for i in range(1,11))),
            'one candidate row removed': ''.join(line for line in lines if not line.startswith('| 10 |')),
            'duplicate title': original.replace(self.titles[1], self.titles[0]),
            'wrong character count': original.replace(f'{len(self.titles[0])}자', '99자'),
            'invented badge': original.replace('블루오션 후보', '무조건 상위 노출'),
            'recommendations removed': ''.join(line for line in lines if not line.startswith('- ')),
        }
        for label, text in variants.items():
            with self.subTest(label=label):
                self.assertNotEqual(original, text)
                path = self.work / 'tampered.md'
                path.write_text(text, encoding='utf-8')
                with self.assertRaises(ValueError):
                    report.check_report(self.work, 'naver', path)

    def test_changed_report_returns_to_title_stage(self):
        self.proposed()
        (self.work / 'naver_report.md').write_text('titles only', encoding='utf-8')
        self.assertEqual(g.next_step(self.work, g.state_of(self.work))[0], 'naver_titles')
        self.assertEqual(self.command('finish', '--reply-file', 'naver_report.md'), 2)

    def test_one_query_for_all_titles_is_rejected(self):
        data = g.read(self.work / 'naver_candidates.json')
        data['search_queries'] = ['fixture exact question'] * 10
        self.put('naver_candidates.json', data)
        with self.assertRaises(ValueError):
            report.expected_report(self.work, 'naver')

    def test_google_complete_report_and_workflow(self):
        self.proposed()
        g.record(self.work, 'naver_selection', [], 'Fixture chosen', 'User chose 1', self.titles[0])
        evidence = g.read(self.work / 'naver_serp_audit.json')
        evidence['channel'] = 'google'
        for row in evidence['records']:
            row['search_url'] = 'https://www.google.com/search?q=' + quote(row['clean_query'])
        self.put('google_serp_audit.json', evidence)
        data = g.read(self.work / 'naver_candidates.json')
        data['google_candidates'] = data.pop('naver_candidates')
        self.put('google_candidates.json', data)
        related = g.read(self.work / 'naver_related_keywords.json')
        related['channel'] = 'google'
        related['records'][0]['source_url'] = 'https://suggestqueries.google.com/complete/search?q=fixture'
        self.put('google_related_keywords.json', related)
        (self.work / 'google_report.md').write_text(report.expected_report(self.work, 'google'), encoding='utf-8')
        from test_reuse_guard import fixture as reuse_fixture
        reuse_fixture(self.work, 'google_titles')
        g.record(self.work, 'google_titles', ['google_candidates.json', 'google_serp_audit.json', 'google_report.md', 'google_related_keywords.json'], 'Fixture Google proposal')
        self.assertEqual(self.command('finish', '--reply-file', 'google_report.md'), 0)
        self.assertEqual(self.command('finish', '--reply-file', 'naver_report.md'), 2)

    def test_existing_format_validator_is_called(self):
        data = g.read(self.work / 'naver_candidates.json')
        for channel in ('naver', 'google'):
            adapted = dict(data, **{channel + '_candidates': self.titles})
            original = getattr(adapter.existing, f'validate_{channel}_titles')
            original_path = adapter.existing.__file__
            with patch.object(adapter.existing, f'validate_{channel}_titles', wraps=original) as reused:
                adapter.check_titles(adapted, channel)
                reused.assert_called_once_with(self.titles, run_serp=False)
            self.assertEqual(adapter.existing.__file__, original_path)

    def test_collector_reused_and_duplicate_queries_collected_once(self):
        self.research()
        data = g.read(self.work / 'naver_candidates.json')
        data['search_queries'][1] = data['search_queries'][0]
        fixture = g.read(self.work / 'naver_serp_audit.json')['records']
        old_dir = adapter.collector.DATA_DIR
        with patch.object(adapter.collector, 'audit_titles', return_value=[r for r in fixture if r['idx'] != 2]) as reused:
            path = adapter.collect(self.work, data, 'naver')
            self.assertEqual(len(reused.call_args.args[0]), 9)
        self.assertEqual(adapter.collector.DATA_DIR, old_dir)
        rows = g.read(path)['records']
        self.assertEqual(len(rows), 10)
        self.assertEqual(rows[0]['clean_query'], rows[1]['clean_query'])
        self.assertNotEqual(rows[0]['title'], rows[1]['title'])

    def test_pending_evidence_never_receives_score_or_recommendation(self):
        evidence = g.read(self.work / 'naver_serp_audit.json')
        evidence['records'][0]['review'] = {}
        self.put('naver_serp_audit.json', evidence)
        text = report.expected_report(self.work, 'naver')
        self.assertIn('| 미확인 |', text)
        self.assertNotIn('**1번**', text)

    def test_reviewed_candidates_reuse_existing_cache_without_network(self):
        self.research()
        data = g.read(self.work / 'naver_candidates.json')
        before = g.read(self.work / 'naver_serp_audit.json')['records']
        with patch.object(adapter.collector, 'fetch_serp', side_effect=AssertionError('Unnecessary recollection')), patch.object(adapter.collector, 'autocomplete', side_effect=AssertionError('Unnecessary autocomplete')), contextlib.redirect_stdout(io.StringIO()):
            path = adapter.collect(self.work, data, 'naver')
        after = g.read(path)['records']
        self.assertEqual([r['collected_at'] for r in before], [r['collected_at'] for r in after])
        self.assertEqual([r['review'] for r in before], [r['review'] for r in after])

    def test_recommendations_follow_existing_score_not_manual_pick(self):
        rows = g.read(self.work / 'naver_serp_audit.json')['records']
        expected = sorted(rows, key=lambda r: adapter.assessed(r)[1], reverse=True)[:3]
        text = report.render(rows, 'naver')
        for i, row in enumerate(expected, 1):
            self.assertIn(f"- {i}픽: **{row['idx']}번**", text)

    def test_medium_competition_can_be_compared_without_blue_ocean(self):
        evidence = g.read(self.work / 'naver_serp_audit.json')
        for row in evidence['records']:
            row['review']['competition'] = 'medium'
        self.put('naver_serp_audit.json', evidence)
        text = report.expected_report(self.work, 'naver')
        (self.work / 'naver_report.md').write_text(text, encoding='utf-8')
        self.proposed()
        self.assertIn('- 1픽:', text)
        self.assertNotIn('🟡 보류', text)

    def test_one_reviewed_query_cannot_pass_comparison(self):
        evidence = g.read(self.work / 'naver_serp_audit.json')
        for row in evidence['records'][1:]:
            row['review'] = {}
        self.put('naver_serp_audit.json', evidence)
        (self.work / 'naver_report.md').write_text(report.expected_report(self.work, 'naver'), encoding='utf-8')
        with self.assertRaises(ValueError):
            self.proposed()

    def test_unreviewed_selected_candidate_blocks_next_stage(self):
        evidence = g.read(self.work / 'naver_serp_audit.json')
        evidence['records'][8]['review'] = {}
        self.put('naver_serp_audit.json', evidence)
        (self.work / 'naver_report.md').write_text(report.expected_report(self.work, 'naver'), encoding='utf-8')
        self.proposed()
        with self.assertRaises(ValueError):
            g.record(self.work, 'naver_selection', [], 'Fixture choice', 'User chose 9', self.titles[8])

    def test_competition_precedes_wording_score(self):
        rows = g.read(self.work / 'naver_serp_audit.json')['records'][:2]
        rows[0]['review']['competition'] = 'medium'
        rows[1]['review']['competition'] = 'gap'
        original = adapter.assessed
        def scores(row):
            result, _ = original(row)
            return result, 100 if row['idx'] == 1 else 40
        with patch.object(adapter, 'assessed', side_effect=scores):
            text = report.render(rows, 'naver')
        self.assertIn('- 1픽: **2번**', text)

    def test_title_comparison_does_not_claim_full_fact_validation(self):
        row = g.read(self.work / 'naver_serp_audit.json')['records'][0]
        row['review'] = {}
        row['title_review'] = {'competition':'medium','reason':'Fixture sampled comparison','reviewed_at':stamp()}
        row['related_keyword'] = {'text':row['clean_query'],'source_url':'https://ac.search.naver.com/nx/ac?q=fixture','observed_at':stamp()}
        result, score = adapter.assessed(row)
        self.assertFalse(result['evidence_complete'])
        self.assertTrue(result['comparison_ready'])
        self.assertIsNotNone(score)
        row['top_docs'] = row['top_docs'][:2]
        result, score = adapter.assessed(row)
        self.assertFalse(result.get('comparison_ready', False))
        self.assertIsNone(score)

    def test_recommendation_queries_are_not_duplicates(self):
        rows = g.read(self.work / 'naver_serp_audit.json')['records']
        rows[1] = dict(copy.deepcopy(rows[0]), idx=2, title=self.titles[1])
        text = report.render(rows, 'naver')
        self.assertNotIn('**2번**', text)
        self.assertIn('- 3픽:', text)

    def test_collect_function_blocks_before_network_when_research_missing(self):
        with patch.object(adapter.collector, 'audit_titles') as network:
            with self.assertRaises(ValueError):
                adapter.collect(self.work, g.read(self.work / 'naver_candidates.json'), 'naver')
            network.assert_not_called()

    def test_google_collect_function_blocks_without_naver_choice(self):
        self.proposed()
        with patch.object(adapter.collector, 'audit_titles') as network:
            with self.assertRaises(ValueError):
                adapter.collect(self.work, {}, 'google')
            network.assert_not_called()

    def test_report_build_blocks_before_write_without_naver_choice(self):
        self.proposed()
        path = self.work / 'google_report.md'
        with self.assertRaises(ValueError):
            report.build_report(self.work, 'google', path)
        self.assertFalse(path.exists())

    def test_related_evidence_missing_blocks_collection(self):
        self.research()
        (self.work / 'naver_related_keywords.json').unlink()
        with patch.object(adapter.collector, 'audit_titles') as network:
            with self.assertRaises(OSError):
                adapter.collect(self.work, g.read(self.work / 'naver_candidates.json'), 'naver')
            network.assert_not_called()

    def test_unobserved_keywords_and_fake_source_rejected(self):
        data = g.read(self.work / 'naver_candidates.json')
        evidence = g.read(self.work / 'naver_related_keywords.json')
        for update in ({'items':['unrelated keyword']}, {'source_url':'https://example.com/fake'}):
            with self.subTest(update=update):
                mutated = copy.deepcopy(evidence)
                mutated['records'][0].update(update)
                self.put('naver_related_keywords.json', mutated)
                with self.assertRaises(ValueError):
                    adapter.check_related_keywords(self.work, data, 'naver')

    def test_registration_blocks_before_existing_function_without_approvals(self):
        import register_post
        self.proposed()
        with patch.object(register_post, 'existing_register') as execute:
            with self.assertRaises(ValueError):
                register_post.register(self.work, 'post_data.json')
            execute.assert_not_called()

    def test_registration_calls_existing_function_only_after_approvals(self):
        import register_post
        self.test_google_complete_report_and_workflow()
        g.record(self.work, 'google_selection', [], 'Fixture choice', 'User chose Google 1', self.titles[0])
        self.make_draft_and_plan()
        self.put('post_data.json', {'title':self.titles[0]})
        with patch.object(register_post, 'existing_register') as execute:
            with self.assertRaises(ValueError):
                register_post.register(self.work, 'post_data.json')
            execute.assert_not_called()
        g.record(self.work, 'image_approval', [], 'Fixture approval', 'User approved fixture plan')
        with patch.object(register_post, 'existing_register') as execute:
            with self.assertRaises(ValueError):
                register_post.register(self.work, 'post_data.json')
            execute.assert_not_called()
        plan = g.read(self.work / 'image_plan.json')
        plan['is_user_approved'] = True
        self.put('image_plan.json', plan)
        from PIL import Image
        from image_guard import REQUIRED_SLOTS
        (self.work / 'images').mkdir()
        for i, name in enumerate(REQUIRED_SLOTS):
            Image.new('RGB', (160, 90), (i * 30, 20, 40)).save(self.work / 'images' / name)
        (self.work / 'naver_final.md').write_text('Fixture final body', encoding='utf-8')
        g.record(self.work, 'assembly', ['post_data.json', 'naver_final.md',
                 *['images/' + n for n in REQUIRED_SLOTS]], 'Fixture images integrated')
        with patch.object(register_post, 'existing_register', return_value=True) as execute:
            register_post.register(self.work, 'post_data.json')
            execute.assert_called_once()
        self.put('post_data.json', {'title':'different title'})
        with patch.object(register_post, 'existing_register') as execute:
            with self.assertRaises(ValueError):
                register_post.register(self.work, 'post_data.json')
            execute.assert_not_called()

    def make_draft_and_plan(self):
        selections = {r['stage']: r.get('selected_title') for r in g.state_of(self.work)['receipts']}
        self.put('post_data.json', {'title': selections['google_selection'], 'bodyHtml': '<p>Fixture full paragraph explaining the topic.</p>'})
        for channel, filename in zip(('naver', 'google'), g.DRAFTS):
            (self.work / filename).write_text('# ' + selections[channel + '_selection'] +
                '\n\nFixture full paragraph explaining the topic.\n', encoding='utf-8')
        from test_reuse_guard import fixture as reuse_fixture
        reuse_fixture(self.work, 'draft')
        g.record(self.work, 'draft', list(g.DRAFTS), 'Fixture body written')
        from image_guard import REQUIRED_SLOTS
        self.put('image_plan.json', {'is_user_approved':False,
            'character_anchor':dict(gender='female',age_range='40',hair='short',
                                   clothing_top='cream blouse',persona_summary='Fixture'),
            'storyboard':[dict(slot=n,type='character' if i in (1,2,3) else 'still_life',
                               prompt='cream blouse fixture') for i,n in enumerate(REQUIRED_SLOTS)]})
        g.record(self.work, 'image_plan', ['image_plan.json', *g.DRAFTS], 'Fixture plan based on body')

    def test_draft_required_before_plan_and_changed_body_invalidates_approval(self):
        self.test_google_complete_report_and_workflow()
        g.record(self.work, 'google_selection', [], 'Choice', 'User chose Google 1', self.titles[0])
        with self.assertRaisesRegex(ValueError, 'draft'):
            g.record(self.work, 'image_plan', ['image_plan.json'], 'Premature plan')
        with self.assertRaises(ValueError):
            g.record(self.work, 'draft', [], 'No body')
        self.make_draft_and_plan()
        g.record(self.work, 'image_approval', [], 'Approved', 'User approved')
        self.assertEqual(g.next_step(self.work, g.state_of(self.work))[0], 'assembly')
        with (self.work / 'google_draft.md').open('a', encoding='utf-8') as f:
            f.write('\nChanged factual explanation')
        self.assertEqual(g.next_step(self.work, g.state_of(self.work))[0], 'draft')

    def test_plan_change_invalidates_approval(self):
        self.test_google_complete_report_and_workflow()
        g.record(self.work, 'google_selection', [], 'Choice', 'User chose Google 1', self.titles[0])
        self.make_draft_and_plan()
        g.record(self.work, 'image_approval', [], 'Approved', 'User approved')
        plan = g.read(self.work / 'image_plan.json')
        plan['storyboard'][0]['prompt'] = 'Changed scene'
        self.put('image_plan.json', plan)
        self.assertEqual(g.next_step(self.work, g.state_of(self.work))[0], 'image_plan')

    def test_migration_preserves_choices_and_tentative_plan(self):
        self.test_google_complete_report_and_workflow()
        g.record(self.work, 'google_selection', [], 'Choice', 'User chose Google 1', self.titles[0])
        old = g.state_of(self.work)
        prefix = copy.deepcopy(old['receipts'])
        old.update(version=1, receipts=prefix + [dict(stage='image_plan', note='Old tentative plan')])
        self.put(g.STATE, old)
        self.put('image_plan.json', {'is_user_approved':False})
        plan_before = (self.work / 'image_plan.json').read_bytes()
        g.migrate_draft_first(self.work)
        state = g.state_of(self.work)
        self.assertEqual(state['receipts'], prefix)
        self.assertEqual(g.next_step(self.work, state)[0], 'draft')
        self.assertEqual((self.work / 'image_plan.json').read_bytes(), plan_before)
        self.assertEqual(g.read(self.work / 'codex_workflow.before_draft_first.json'), old)
        g.migrate_draft_first(self.work)
        self.assertEqual(g.state_of(self.work), state)


if __name__ == '__main__':
    unittest.main()
