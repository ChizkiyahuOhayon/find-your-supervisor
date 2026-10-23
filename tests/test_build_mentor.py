import importlib.util
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
spec=importlib.util.spec_from_file_location('build_mentor',ROOT/'scripts'/'build_mentor.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture():
    import audit
    d=audit.fresh('Example Scholar','example-scholar')
    d['researcher']['identity_confirmed']=True
    d['researcher']['sources_checked']=['catalog1','catalog2']
    for i in (1,2):
        d['papers'].append({'canonical_id':f'id:{i}','title':f'Test paper {i}','year':2025,
                          'url':f'https://example.org/{i}','author_identity_verified':True,
                          'main_pdf':{'pages_read':[1]},'claimed_stage':'selected_pages'})
    dna={'schema_version':'1.0.0','researcher_slug':'example-scholar','principles':[
        {'id':'P1','principle':'A stated research strategy','supporting_paper_ids':['id:1','id:2'],
         'confidence':'hypothesis','student_application':'Use an explicit minimal baseline',
         'falsification_test':'Compare against a frozen baseline'}]}
    return d,dna


class BuildMentorTest(unittest.TestCase):
    def test_happy_path(self):
        d,dna=fixture()
        self.assertEqual([],m.check(d,dna))
        result=m.compile_markdown(d,dna)
        self.assertIn('non-impersonating',result)
        self.assertIn('P1',result)
        self.assertIn('GO / REVISE',result)

    def test_identity_is_gate(self):
        d,dna=fixture()
        d['researcher']['identity_confirmed']=False
        self.assertTrue(any('identity' in x for x in m.check(d,dna)))

    def test_one_paper_is_not_general_pattern(self):
        d,dna=fixture()
        dna['principles'][0]['supporting_paper_ids']=['id:1']
        self.assertTrue(any('two distinct' in x for x in m.check(d,dna)))

    def test_metadata_not_full_read(self):
        d,dna=fixture()
        del d['papers'][0]['main_pdf']
        self.assertTrue(any('page-level' in x for x in m.check(d,dna)))

    def test_strong_requires_main_full(self):
        d,dna=fixture()
        dna['principles'][0]['confidence']='strong'
        self.assertTrue(any('strong requires' in x for x in m.check(d,dna)))

    def test_unverified_authorship(self):
        d,dna=fixture()
        d['papers'][0]['author_identity_verified']=False
        self.assertTrue(any('authorship' in x for x in m.check(d,dna)))


if __name__ == '__main__':
    unittest.main()
