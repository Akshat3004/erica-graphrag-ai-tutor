import unittest
from erica.graph import build_graph
from erica.retrieval import retrieve
from erica.cli import respond

class EricaSmokeTest(unittest.TestCase):
    def setUp(self):
        self.graph=build_graph([{'url':'https://example.org/attention','title':'Attention','text':'A transformer uses attention to weigh tokens.'}])
    def test_retrieval(self):
        r=retrieve(self.graph,'What is attention?')
        self.assertIn('attention',r['concepts'])
        self.assertEqual(r['pages'][0]['url'],'https://example.org/attention')
    def test_offline_generation(self):
        r=respond(self.graph,'Explain transformer attention',offline=True)
        self.assertIn('Offline retrieval preview',r['answer'])
    def test_unsupported(self):
        r=respond(self.graph,'What is quantum tunneling?',offline=True)
        self.assertEqual(r['pages'],[])
        self.assertIn("couldn't find",r['answer'])
if __name__=='__main__':unittest.main()
