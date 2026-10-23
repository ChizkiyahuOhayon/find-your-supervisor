import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('adapters',ROOT/'scripts'/'adapters.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class AdapterTest(unittest.TestCase):
    def test_all_tasks_have_routes(self):
        data=m.manifest()
        self.assertTrue(data['tasks'])
        for task in data['tasks']:
            self.assertTrue(m.candidates(task,{}))

    def test_installed_candidate(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'ccf-idea-reviewer'/'SKILL.md'
            p.parent.mkdir(parents=True)
            p.write_text('# fake test fixture')
            out=m.candidates('idea-review',{'ccfa':Path(d)})
            self.assertTrue(out[0]['available'])
            self.assertFalse(out[1]['available'])

    def test_unknown_task(self):
        with self.assertRaises(ValueError):
            m.candidates('../evil',{})

    def test_traversal_manifest(self):
        data={'sources':{'test':{'license':'x'}},'tasks':{'test':[{'source':'test','path':'../outside'}]}}
        with self.assertRaises(ValueError):
            m.candidates('test',{},data)

    def test_symlink_escape(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            external=p/'external'
            external.mkdir()
            (external/'SKILL.md').write_text('bad')
            fake=p/'internal'
            fake.mkdir()
            (fake/'outside').symlink_to(external,target_is_directory=True)
            data={'sources':{'test':{'license':'x'}},'tasks':{'test':[{'source':'test','path':'outside/SKILL.md'}]}}
            out=m.candidates('test',{'test':fake},data)
            self.assertFalse(out[0]['available'])


if __name__ == '__main__':
    unittest.main()
