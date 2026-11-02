"""CLI demonstration with optional local LLM generation."""
import argparse
from erica.graph import load_graph
from erica.retrieval import retrieve
from erica import llm

def respond(graph, question, offline=False, embed=None, generate=None):
    retrieval=retrieve(graph,question,embed=embed if embed is not None else (None if offline else llm.embed))
    if not retrieval['concepts']:
        return {'answer':"I couldn't find relevant concepts in this dataset.",**retrieval}
    if offline:
        result='Offline retrieval preview — no model answer generated.'
    else:
        prompt=("You are Erica, an AI tutor. Answer using only the context below. "
                "If the context does not answer the question, say you lack evidence. "
                "Do not invent citations.\nCONTEXT:\n"+retrieval['context'][:8000]+"\nQUESTION:\n"+question)
        result=(generate or llm.answer)(prompt)
    return {'answer':result,**retrieval}

def main():
    parser=argparse.ArgumentParser(description='Erica GraphRAG demo')
    parser.add_argument('--graph',default='erica/data/demo_graph.json')
    parser.add_argument('--query')
    parser.add_argument('--offline',action='store_true')
    opts=parser.parse_args()
    graph=load_graph(opts.graph)
    questions=[opts.query] if opts.query else iter(lambda:input('You (exit to quit): ').strip(), 'exit')
    for question in questions:
        result=respond(graph,question,offline=opts.offline)
        print('\nErica:',result['answer'])
        print('Matched concepts:',', '.join(result['concepts']) or '(none)')
        print('Source URLs (retrieved, not fact-checked):')
        for page in result['pages'][:5]:print('-',page['url'])
        print()
if __name__=='__main__':main()
