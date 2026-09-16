import copy
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import freshness_guard as f


def fixture(work, day=None):
    day = day or f.today()
    text = 'Fixture observed search and source. Published ' + day.isoformat()
    (work / 'observed.txt').write_text(text, encoding='utf-8')
    proof = dict(evidence_file='observed.txt', evidence_sha256=hashlib.sha256(text.encode()).hexdigest(), evidence_excerpt=text)
    data = {'schema_version':1, 'checked_on':str(day), 'searches':[
        dict(proof, id='recent', query='fixture food safety', url='https://www.google.com/search?q=fixture', searched_on=str(day), purpose='recent_discovery', channel='google', **{'from':str(f.window_start(day)), 'to':str(day)})],
        'sources':[dict(proof, id='fact1', title='Fixture source', url='https://example.org/source', accessed_on=str(day), role='fact', published_on=str(day), date_evidence=str(day))],
        'claims':[{'text':'Fixture claim','source_ids':['fact1']}]}
    (work / f.MANIFEST).write_text(json.dumps(data),encoding='utf-8')
    return data


class Freshness(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.work = Path(self.tmp.name)
        self.day = date(2026,9,14)
        self.data = fixture(self.work,self.day)

    def check(self):
        (self.work/f.MANIFEST).write_text(json.dumps(self.data),encoding='utf-8')
        return f.validate(self.work,self.day)

    def test_calendar_rollover(self):
        self.assertEqual(f.window_start(date(2027,1,8)),date(2026,11,1))
        self.assertEqual(f.window_start(self.day),date(2026,7,1))

    def test_valid_recent(self):
        self.assertIn('observed.txt',self.check())

    def test_missing_and_changed_evidence(self):
        (self.work/f.MANIFEST).unlink()
        with self.assertRaises(ValueError):f.validate(self.work,self.day)
        (self.work/'observed.txt').write_text('changed',encoding='utf-8')
        with self.assertRaises(ValueError):self.check()

    def test_recent_access_does_not_make_old_publication_recent(self):
        self.data['sources'][0]['published_on']='2023-01-01'
        with self.assertRaisesRegex(ValueError,'사용 이유'):self.check()

    def test_old_source_needs_validity_search(self):
        row=self.data['sources'][0]
        row.update(published_on=None,date_status='unknown',exception_reason='Still useful',validity_note='Checked guidance')
        with self.assertRaisesRegex(ValueError,'유효성'):self.check()
        search=copy.deepcopy(self.data['searches'][0])
        search.update(id='verify',purpose='validity_check',result='Fixture no replacement found')
        self.data['searches'].append(search)
        row['validity_search_id']='verify'
        self.check()

    def test_zero_recent_sources_allowed_with_documented_old_source(self):
        # Recent discovery may find nothing suitable; an old, checked source
        # must remain usable without inventing a recent publication.
        text = 'Fixture recent search: no suitable new source. Original publication 2022-06-20. Validity search: no replacement found.'
        (self.work/'observed.txt').write_text(text,encoding='utf-8')
        proof = dict(evidence_file='observed.txt',evidence_sha256=hashlib.sha256(text.encode()).hexdigest(),evidence_excerpt=text)
        self.data['searches'][0].update(proof,result='No suitable recent source')
        search=copy.deepcopy(self.data['searches'][0])
        search.update(id='verify-old',purpose='validity_check',result='Fixture existing guidance still applies')
        self.data['searches'].append(search)
        self.data['sources'][0].update(proof,published_on='2022-06-20',date_evidence='2022-06-20',exception_reason='Relevant existing official guidance; no suitable newer replacement',validity_search_id='verify-old',validity_note='Checked for revisions and replacement')
        self.assertIn(f.MANIFEST,self.check())
        del self.data['sources'][0]['exception_reason']
        with self.assertRaisesRegex(ValueError,'사용 이유'):self.check()

    def test_future_and_unverified_update(self):
        row=self.data['sources'][0]
        row['published_on']=str(self.day+timedelta(days=1))
        with self.assertRaisesRegex(ValueError,'미래'):self.check()
        row.update(published_on='2023-01-01',updated_on=str(self.day),substantive_update=False)
        with self.assertRaisesRegex(ValueError,'사용 이유'):self.check()

    def test_window_and_wrong_claim(self):
        self.data['searches'][0]['from']='2026-08-01'
        with self.assertRaises(ValueError):self.check()
        self.data['searches'][0]['from']='2026-07-01'
        self.data['claims'][0]['source_ids']=['invented']
        with self.assertRaisesRegex(ValueError,'근거 ID'):self.check()

    def test_no_search_or_stale_check(self):
        self.data['checked_on']='2026-09-13'
        with self.assertRaises(ValueError):self.check()
        self.data['checked_on']=str(self.day)
        self.data['searches']=[]
        with self.assertRaises(ValueError):self.check()

    def test_path_escape(self):
        self.data['sources'][0]['evidence_file']='../outside.txt'
        with self.assertRaises(ValueError):self.check()

    def test_registration_blocked_even_at_correct_stage(self):
        import register_post
        (self.work/f.MANIFEST).unlink()
        with patch('workflow_guard.next_step',return_value=('validation','')), patch.object(register_post,'existing_register') as write:
            with self.assertRaisesRegex(ValueError,'최신성'):
                register_post.register(self.work,'not-created.json')
            write.assert_not_called()

    def test_research_record_blocked_without_manifest(self):
        import workflow_guard as g
        (self.work/f.MANIFEST).unlink()
        with patch.object(g,'next_step',return_value=('research','')):
            with self.assertRaisesRegex(ValueError,'최신성'):
                g.record(self.work,'research',[],'attempt')


if __name__ == '__main__':unittest.main()
