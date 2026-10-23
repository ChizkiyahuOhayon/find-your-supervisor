import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
spec = importlib.util.spec_from_file_location('supervisor', ROOT/'scripts'/'supervisor.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SupervisorCLITest(unittest.TestCase):
    def test_workspace_creation_and_private_location(self):
        with tempfile.TemporaryDirectory() as d:
            p = m.make_workspace(d, 'Example Scholar', 'example-scholar')
            self.assertTrue((p/'researcher.json').exists())
            self.assertFalse(json.loads((p/'researcher.json').read_text())['researcher']['identity_confirmed'])
            with self.assertRaises(FileExistsError):
                m.make_workspace(d, 'Example Scholar', 'example-scholar')

    def test_import_and_dedupe(self):
        with tempfile.TemporaryDirectory() as d:
            p = m.make_workspace(d, 'Example Scholar', 'example-scholar')
            a = m.load(p/'researcher.json')
            stats = m.import_csv(a, ROOT/'examples'/'synthetic-publications.csv', 'example')
            self.assertEqual(2, stats['added'])
            self.assertEqual(1, stats['duplicate_keys'])
            self.assertEqual('metadata_only', a['papers'][0]['claimed_stage'])
            self.assertFalse(a['papers'][0]['author_identity_verified'])
            self.assertTrue(any('identity' in text.lower() for text in m.next_steps(a)))

    def test_no_source_name(self):
        with tempfile.TemporaryDirectory() as d:
            p=m.make_workspace(d,'A','a')
            with self.assertRaises(ValueError):
                m.import_csv(m.load(p/'researcher.json'),ROOT/'examples'/'synthetic-publications.csv','')

    def test_title_fallback_canonical(self):
        self.assertEqual(m.record_key({'title':'My New Paper','year':'2024'}), m.record_key({'title':'My-New Paper!','year':'2024'}))

    def test_doi_canonical(self):
        self.assertEqual(m.record_key({'doi':'https://doi.org/10.5555/XYZ'}), m.record_key({'doi':'10.5555/xyz'}))

    def test_public_directory_protection(self):
        with self.assertRaises(ValueError):
            m.make_workspace(ROOT/'profiles','A','a')


if __name__ == '__main__':
    unittest.main()
