import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import source_access_guard as guard
import workflow_guard as workflow

class AccessTests(unittest.TestCase):
    def test_phase_lifecycle_and_network_block(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            with patch('urllib.request.urlopen') as net:
                with self.assertRaises(PermissionError):
                    guard.fetch(w, 'https://example.com/source')
                net.assert_not_called()
            with self.assertRaises(ValueError):
                guard.transition(w, 'research', 'skip')
            guard.transition(w, 'titles', 'user chose topic')
            with self.assertRaises(PermissionError):
                guard.authorize(w, 'source')
            with self.assertRaises(ValueError):
                guard.transition(w, 'research', 'missing titles')
            guard.transition(w, 'research', 'user selected both', 'naver', 'google')
            source = w / 'original.txt'
            source.write_text('verified source', encoding='utf-8')
            self.assertEqual(guard.fetch(w, str(source)), 'verified source')
            with self.assertRaises(ValueError):
                guard.transition(w, 'writing', 'missing notes')
            (w / 'source_notes.md').write_text('summary', encoding='utf-8')
            guard.transition(w, 'writing', 'research complete')
            with self.assertRaises(PermissionError):
                guard.fetch(w, str(source))
            guard.transition(w, 'research', 'missing evidence for claim')
            guard.authorize(w, str(source))
            self.assertIn('false', (w / 'source_access_log.jsonl').read_text(encoding='utf-8'))

    def test_titles_precede_research(self):
        self.assertLess(workflow.STEPS.index('google_selection'), workflow.STEPS.index('research'))
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(workflow.next_step(Path(d), workflow.state_of(Path(d)))[0], 'naver_titles')

    def test_title_validation_does_not_require_body_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            w = Path(d)
            (w / 'naver_candidates.json').write_text('{}', encoding='utf-8')
            with patch.object(workflow, 'titles_check') as check:
                workflow.validate_artifacts(w, 'naver_titles', ['naver_candidates.json'])
                check.assert_called_once()

if __name__ == '__main__':
    unittest.main()
